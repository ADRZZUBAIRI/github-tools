<?php
/**
 * Dispatch Engine with WP-Cron Retry Queue and Logging
 */

if (!defined('ABSPATH')) {
    exit;
}

class WLR_Dispatcher {

    /**
     * Dispatch lead payload to configured webhook endpoints
     */
    public static function dispatch($lead_data, $form_source = 'Unknown') {
        $settings = get_option(WLR_OPTION_SETTINGS, array());
        $primary_url = isset($settings['primary_webhook']) ? esc_url_raw($settings['primary_webhook']) : '';

        if (empty($primary_url)) {
            return false;
        }

        // Apply E.164 phone normalization if enabled
        if (!empty($settings['normalize_phone'])) {
            $default_country = !empty($settings['default_country']) ? $settings['default_country'] : 'US';
            foreach (array('phone', 'telephone', 'mobile', 'cell', 'contact_number') as $phone_key) {
                if (isset($lead_data[$phone_key])) {
                    $lead_data[$phone_key] = WLR_Sanitizer::normalize_phone($lead_data[$phone_key], $default_country);
                }
            }
        }

        // Standardize uniform payload envelope
        $payload = array(
            'event'          => 'contractor.lead.received',
            'timestamp'      => current_time('mysql'),
            'timestamp_iso'  => gmdate('c'),
            'source_site'    => get_bloginfo('name'),
            'site_url'       => get_site_url(),
            'form_source'    => sanitize_text_field($form_source),
            'lead_data'      => WLR_Sanitizer::sanitize_payload($lead_data),
            'client_ip'      => self::get_client_ip(),
            'user_agent'     => isset($_SERVER['HTTP_USER_AGENT']) ? sanitize_text_field(wp_unslash($_SERVER['HTTP_USER_AGENT'])) : ''
        );

        // Allow developers to filter the payload
        $payload = apply_filters('wlr_before_dispatch', $payload, $form_source);

        // Execute primary dispatch
        $start_time = microtime(true);
        $response = self::send_request($primary_url, $payload, $settings);
        $duration_ms = round((microtime(true) - $start_time) * 1000, 2);

        $success = false;
        $http_code = 0;
        $response_body = '';

        if (is_wp_error($response)) {
            $response_body = $response->get_error_message();
        } else {
            $http_code = wp_remote_retrieve_response_code($response);
            $response_body = wp_remote_retrieve_body($response);
            if ($http_code >= 200 && $http_code < 300) {
                $success = true;
            }
        }

        // If primary failed and fallback configured, try fallback
        if (!$success && !empty($settings['fallback_webhook'])) {
            $fallback_url = esc_url_raw($settings['fallback_webhook']);
            $fallback_response = self::send_request($fallback_url, $payload, $settings);
            if (!is_wp_error($fallback_response)) {
                $fallback_code = wp_remote_retrieve_response_code($fallback_response);
                if ($fallback_code >= 200 && $fallback_code < 300) {
                    $success = true;
                    $http_code = $fallback_code;
                    $response_body = 'Delivered to fallback endpoint: ' . wp_remote_retrieve_body($fallback_response);
                }
            }
        }

        // If still failed, push to WP-Cron retry queue
        if (!$success) {
            self::enqueue_retry($payload, $primary_url);
        }

        // Record visual telemetry log
        self::log_dispatch(array(
            'timestamp'    => current_time('mysql'),
            'form_source'  => $form_source,
            'lead_name'    => self::extract_lead_name($lead_data),
            'lead_phone'   => self::extract_lead_phone($lead_data),
            'status'       => $success ? 'SUCCESS' : 'FAILED',
            'http_code'    => $http_code,
            'latency_ms'   => $duration_ms,
            'response'     => substr($response_body, 0, 500)
        ));

        do_action('wlr_after_dispatch', $payload, $success, $http_code);

        return $success;
    }

    private static function send_request($url, $payload, $settings) {
        $headers = array(
            'Content-Type' => 'application/json; charset=utf-8',
            'User-Agent'   => 'WebSmitherz-Lead-Dispatcher/' . WLR_VERSION
        );

        if (!empty($settings['auth_bearer_token'])) {
            $headers['Authorization'] = 'Bearer ' . sanitize_text_field($settings['auth_bearer_token']);
        }

        // Custom headers parsing
        if (!empty($settings['custom_headers'])) {
            $lines = explode("\n", $settings['custom_headers']);
            foreach ($lines as $line) {
                $parts = explode(':', $line, 2);
                if (count($parts) === 2) {
                    $headers[trim($parts[0])] = trim($parts[1]);
                }
            }
        }

        return wp_remote_post($url, array(
            'headers'     => $headers,
            'body'        => wp_json_encode($payload),
            'timeout'     => 15,
            'redirection' => 3,
            'blocking'    => true
        ));
    }

    private static function enqueue_retry($payload, $target_url) {
        $queue = get_option('wlr_retry_queue', array());
        if (count($queue) > 50) {
            array_shift($queue); // keep max 50 items
        }
        $queue[] = array(
            'payload'    => $payload,
            'url'        => $target_url,
            'attempts'   => 1,
            'first_try'  => time(),
            'last_try'   => time()
        );
        update_option('wlr_retry_queue', $queue);
    }

    public static function process_retry_queue() {
        $queue = get_option('wlr_retry_queue', array());
        if (empty($queue)) {
            return;
        }

        $settings = get_option(WLR_OPTION_SETTINGS, array());
        $max_attempts = isset($settings['retry_attempts']) ? intval($settings['retry_attempts']) : 3;
        $remaining = array();

        foreach ($queue as $item) {
            if ($item['attempts'] >= $max_attempts) {
                continue; // drop expired retry
            }

            $response = self::send_request($item['url'], $item['payload'], $settings);
            if (!is_wp_error($response) && wp_remote_retrieve_response_code($response) >= 200 && wp_remote_retrieve_response_code($response) < 300) {
                // Succeeded on retry
                self::log_dispatch(array(
                    'timestamp'    => current_time('mysql'),
                    'form_source'  => $item['payload']['form_source'] . ' (Retry #' . $item['attempts'] . ')',
                    'lead_name'    => self::extract_lead_name($item['payload']['lead_data']),
                    'lead_phone'   => self::extract_lead_phone($item['payload']['lead_data']),
                    'status'       => 'SUCCESS',
                    'http_code'    => wp_remote_retrieve_response_code($response),
                    'latency_ms'   => 0,
                    'response'     => 'Recovered on cron retry'
                ));
            } else {
                $item['attempts']++;
                $item['last_try'] = time();
                $remaining[] = $item;
            }
        }

        update_option('wlr_retry_queue', $remaining);
    }

    private static function log_dispatch($entry) {
        $logs = get_option(WLR_OPTION_LOGS, array());
        array_unshift($logs, $entry);
        if (count($logs) > 100) {
            $logs = array_slice($logs, 0, 100);
        }
        update_option(WLR_OPTION_LOGS, $logs);
    }

    private static function extract_lead_name($data) {
        foreach (array('name', 'full_name', 'your_name', 'first_name', 'fname') as $k) {
            if (!empty($data[$k])) {
                return sanitize_text_field($data[$k]);
            }
        }
        return 'Prospective Client';
    }

    private static function extract_lead_phone($data) {
        foreach (array('phone', 'telephone', 'mobile', 'cell', 'phone_number') as $k) {
            if (!empty($data[$k])) {
                return sanitize_text_field($data[$k]);
            }
        }
        return 'N/A';
    }

    private static function get_client_ip() {
        if (!empty($_SERVER['HTTP_CF_CONNECTING_IP'])) {
            return sanitize_text_field($_SERVER['HTTP_CF_CONNECTING_IP']);
        }
        if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
            $parts = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
            return sanitize_text_field(trim($parts[0]));
        }
        return isset($_SERVER['REMOTE_ADDR']) ? sanitize_text_field($_SERVER['REMOTE_ADDR']) : '';
    }
}
