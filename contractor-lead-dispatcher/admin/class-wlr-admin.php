<?php
/**
 * Admin Settings, Telemetry Dashboard & Architecture Audit Card
 */

if (!defined('ABSPATH')) {
    exit;
}

class WLR_Admin {

    public static function init() {
        add_action('admin_menu', array(__CLASS__, 'register_admin_menu'));
        add_action('admin_init', array(__CLASS__, 'register_settings'));
        add_action('admin_post_wlr_send_test_lead', array(__CLASS__, 'handle_test_lead'));
        add_action('admin_post_wlr_clear_logs', array(__CLASS__, 'handle_clear_logs'));
    }

    public static function register_admin_menu() {
        add_menu_page(
            __('Contractor Lead Dispatcher', 'contractor-lead-dispatcher'),
            __('Lead Dispatcher', 'contractor-lead-dispatcher'),
            'manage_options',
            'contractor-lead-dispatcher',
            array(__CLASS__, 'render_admin_page'),
            'dashicons-rest-api',
            58
        );
    }

    public static function register_settings() {
        register_setting('wlr_settings_group', WLR_OPTION_SETTINGS, array(__CLASS__, 'sanitize_settings'));
    }

    public static function sanitize_settings($input) {
        $output = array();
        $output['primary_webhook']   = isset($input['primary_webhook']) ? esc_url_raw($input['primary_webhook']) : '';
        $output['fallback_webhook']  = isset($input['fallback_webhook']) ? esc_url_raw($input['fallback_webhook']) : '';
        $output['auth_bearer_token'] = isset($input['auth_bearer_token']) ? sanitize_text_field($input['auth_bearer_token']) : '';
        $output['custom_headers']    = isset($input['custom_headers']) ? sanitize_textarea_field($input['custom_headers']) : '';
        $output['normalize_phone']   = !empty($input['normalize_phone']) ? 1 : 0;
        $output['default_country']   = isset($input['default_country']) ? sanitize_text_field($input['default_country']) : 'US';
        $output['retry_attempts']    = isset($input['retry_attempts']) ? max(1, min(10, intval($input['retry_attempts']))) : 3;
        return $output;
    }

    public static function handle_test_lead() {
        check_admin_referer('wlr_test_lead_action');
        if (!current_user_can('manage_options')) {
            wp_die(__('Unauthorized user.', 'contractor-lead-dispatcher'));
        }

        $test_data = array(
            'full_name'    => 'John Doe (Test Contractor Lead)',
            'phone'        => '2145550198',
            'email'        => 'test.lead@example.com',
            'service_type' => 'Emergency Hail Roof Inspection & Reroof',
            'address'      => '742 Evergreen Terrace, Dallas, TX 75201',
            'notes'        => 'Simulated test dispatch from Lead Dispatcher settings dashboard.'
        );

        $result = WLR_Dispatcher::dispatch($test_data, 'Dashboard Diagnostic Test');

        $redirect = add_query_arg(array(
            'page'        => 'contractor-lead-dispatcher',
            'test_status' => $result ? 'success' : 'failed'
        ), admin_url('admin.php'));

        wp_safe_redirect($redirect);
        exit;
    }

    public static function handle_clear_logs() {
        check_admin_referer('wlr_clear_logs_action');
        if (!current_user_can('manage_options')) {
            wp_die(__('Unauthorized user.', 'contractor-lead-dispatcher'));
        }

        update_option(WLR_OPTION_LOGS, array());

        wp_safe_redirect(add_query_arg(array('page' => 'contractor-lead-dispatcher', 'logs_cleared' => 1), admin_url('admin.php')));
        exit;
    }

    public static function render_admin_page() {
        $settings = get_option(WLR_OPTION_SETTINGS, array());
        $logs = get_option(WLR_OPTION_LOGS, array());
        $retry_queue = get_option('wlr_retry_queue', array());
        ?>
        <div class="wrap" style="max-width: 1100px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #ddd;">
                <div>
                    <h1 style="font-size: 24px; font-weight: 700; color: #111; margin: 0;">Contractor Lead Dispatcher &amp; Instant Webhooks</h1>
                    <p style="color: #666; margin: 4px 0 0 0; font-size: 13px;">Sub-60s webhook dispatch engine for ServiceTitan, Jobber, AccuLynx, and trade CRMs.</p>
                </div>
                <div style="font-size: 12px; font-family: monospace; background: #eef2ff; color: #4338ca; padding: 6px 12px; border-radius: 6px; border: 1px solid #c7d2fe;">
                    v<?php echo esc_html(WLR_VERSION); ?> &middot; System Status: Active
                </div>
            </div>

            <?php if (isset($_GET['test_status'])): ?>
                <?php if ($_GET['test_status'] === 'success'): ?>
                    <div class="notice notice-success is-dismissible" style="border-left-color: #10b981;">
                        <p><strong>Success:</strong> Test lead payload dispatched successfully to your primary webhook endpoint.</p>
                    </div>
                <?php else: ?>
                    <div class="notice notice-error is-dismissible" style="border-left-color: #ef4444;">
                        <p><strong>Dispatch Alert:</strong> Primary webhook test failed. Check endpoint URL and response status in the telemetry table below.</p>
                    </div>
                <?php endif; ?>
            <?php endif; ?>

            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px;">
                <!-- LEFT COLUMN: WEBHOOK CONFIGURATION -->
                <div>
                    <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 24px;">
                        <h2 style="font-size: 16px; font-weight: 600; margin-top: 0; margin-bottom: 16px; color: #1e293b;">Webhook Target Endpoints</h2>
                        
                        <form method="post" action="options.php">
                            <?php settings_fields('wlr_settings_group'); ?>
                            
                            <table class="form-table" style="margin-top: 0;">
                                <tr>
                                    <th scope="row" style="font-size: 13px;"><label for="primary_webhook">Primary CRM Webhook *</label></th>
                                    <td>
                                        <input type="url" id="primary_webhook" name="<?php echo esc_attr(WLR_OPTION_SETTINGS); ?>[primary_webhook]" value="<?php echo esc_attr(isset($settings['primary_webhook']) ? $settings['primary_webhook'] : ''); ?>" class="large-text" placeholder="https://api.servicetitan.io/webhooks/leads or Zapier / Make hook" required style="border-radius: 6px; padding: 6px 10px;">
                                        <p class="description" style="font-size: 12px; color: #64748b;">Submissions will be dispatched as standard JSON payloads to this endpoint within milliseconds.</p>
                                    </td>
                                </tr>

                                <tr>
                                    <th scope="row" style="font-size: 13px;"><label for="fallback_webhook">Secondary Failover Webhook</label></th>
                                    <td>
                                        <input type="url" id="fallback_webhook" name="<?php echo esc_attr(WLR_OPTION_SETTINGS); ?>[fallback_webhook]" value="<?php echo esc_attr(isset($settings['fallback_webhook']) ? $settings['fallback_webhook'] : ''); ?>" class="large-text" placeholder="Optional backup webhook URL" style="border-radius: 6px; padding: 6px 10px;">
                                        <p class="description" style="font-size: 12px; color: #64748b;">If the primary CRM returns a 5xx error or connection timeout, payload routes here automatically.</p>
                                    </td>
                                </tr>

                                <tr>
                                    <th scope="row" style="font-size: 13px;"><label for="auth_bearer_token">Bearer Authorization Token</label></th>
                                    <td>
                                        <input type="password" id="auth_bearer_token" name="<?php echo esc_attr(WLR_OPTION_SETTINGS); ?>[auth_bearer_token]" value="<?php echo esc_attr(isset($settings['auth_bearer_token']) ? $settings['auth_bearer_token'] : ''); ?>" class="regular-text" placeholder="Optional Secret or API Key" style="border-radius: 6px; padding: 6px 10px;">
                                        <p class="description" style="font-size: 12px; color: #64748b;">Appended as <code>Authorization: Bearer [token]</code> header.</p>
                                    </td>
                                </tr>

                                <tr>
                                    <th scope="row" style="font-size: 13px;">E.164 Phone Normalization</th>
                                    <td>
                                        <label>
                                            <input type="checkbox" name="<?php echo esc_attr(WLR_OPTION_SETTINGS); ?>[normalize_phone]" value="1" <?php checked(!empty($settings['normalize_phone'])); ?>>
                                            Automatically format numbers into international E.164 (e.g. <code>+12145550198</code>)
                                        </label>
                                        <p class="description" style="font-size: 12px; color: #64748b;">Critical for instant SMS lead alerts and Twilio / ServiceTitan routing.</p>
                                    </td>
                                </tr>

                                <tr>
                                    <th scope="row" style="font-size: 13px;"><label for="custom_headers">Custom Headers (1 per line)</label></th>
                                    <td>
                                        <textarea id="custom_headers" name="<?php echo esc_attr(WLR_OPTION_SETTINGS); ?>[custom_headers]" rows="3" class="large-text" placeholder="X-Contractor-ID: 84920&#10;X-Client-Region: Dallas" style="border-radius: 6px;"><?php echo esc_textarea(isset($settings['custom_headers']) ? $settings['custom_headers'] : ''); ?></textarea>
                                    </td>
                                </tr>
                            </table>

                            <?php submit_button(__('Save Webhook Configuration', 'contractor-lead-dispatcher'), 'primary', 'submit', false, array('style' => 'border-radius: 6px; padding: 6px 18px; font-weight: 600;')); ?>
                        </form>
                    </div>

                    <!-- RECENT TELEMETRY LOG -->
                    <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <h2 style="font-size: 16px; font-weight: 600; margin: 0; color: #1e293b;">Live Dispatch Telemetry (Last 100 Leads)</h2>
                            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin: 0;">
                                <?php wp_nonce_field('wlr_clear_logs_action'); ?>
                                <input type="hidden" name="action" value="wlr_clear_logs">
                                <button type="submit" class="button button-secondary" style="font-size: 11px; padding: 2px 8px; border-radius: 4px;">Clear Telemetry</button>
                            </form>
                        </div>

                        <?php if (empty($logs)): ?>
                            <p style="color: #94a3b8; font-size: 13px; text-align: center; padding: 24px 0;">No form leads dispatched yet. Submit a test form below or wait for visitor inquiries.</p>
                        <?php else: ?>
                            <div style="overflow-x: auto;">
                                <table class="widefat striped" style="border: 1px solid #e2e8f0; border-radius: 6px; font-size: 12px;">
                                    <thead>
                                        <tr>
                                            <th>Timestamp</th>
                                            <th>Lead / Phone</th>
                                            <th>Source Form</th>
                                            <th>Status</th>
                                            <th>HTTP</th>
                                            <th>Latency</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach (array_slice($logs, 0, 15) as $log): ?>
                                            <tr>
                                                <td style="font-family: monospace;"><?php echo esc_html($log['timestamp']); ?></td>
                                                <td>
                                                    <strong><?php echo esc_html($log['lead_name']); ?></strong><br>
                                                    <span style="color: #64748b; font-family: monospace;"><?php echo esc_html($log['lead_phone']); ?></span>
                                                </td>
                                                <td style="color: #475569;"><?php echo esc_html($log['form_source']); ?></td>
                                                <td>
                                                    <?php if ($log['status'] === 'SUCCESS'): ?>
                                                        <span style="color: #059669; font-weight: bold; background: #ecfdf5; padding: 2px 6px; border-radius: 4px; border: 1px solid #a7f3d0;">OK</span>
                                                    <?php else: ?>
                                                        <span style="color: #dc2626; font-weight: bold; background: #fef2f2; padding: 2px 6px; border-radius: 4px; border: 1px solid #fecaca;">FAIL</span>
                                                    <?php endif; ?>
                                                </td>
                                                <td style="font-family: monospace;"><?php echo esc_html($log['http_code']); ?></td>
                                                <td style="font-family: monospace;"><?php echo esc_html($log['latency_ms']); ?> ms</td>
                                            </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            </div>
                        <?php endif; ?>
                    </div>
                </div>

                <!-- RIGHT COLUMN: ACTION SANDBOX & WEBSMITHERZ ARCHITECTURE BADGE -->
                <div>
                    <!-- TEST SIMULATOR CARD -->
                    <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 24px;">
                        <h3 style="font-size: 14px; font-weight: 600; margin-top: 0; color: #1e293b;">Diagnostic Test Simulator</h3>
                        <p style="font-size: 12px; color: #64748b; line-height: 1.5;">
                            Send a simulated high-ticket emergency roof estimate lead through your configured webhook to verify connectivity and schema reception.
                        </p>
                        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                            <?php wp_nonce_field('wlr_test_lead_action'); ?>
                            <input type="hidden" name="action" value="wlr_send_test_lead">
                            <button type="submit" class="button button-primary" style="width: 100%; border-radius: 6px; font-weight: 600; text-align: center; justify-content: center; display: flex;">
                                Dispatch Simulated Lead &rarr;
                            </button>
                        </form>
                    </div>

                    <!-- FAILOVER QUEUE STATUS -->
                    <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 24px;">
                        <h3 style="font-size: 14px; font-weight: 600; margin-top: 0; color: #1e293b;">Offline Retry Queue</h3>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                            <span style="font-size: 12px; color: #64748b;">Pending Dispatches:</span>
                            <span style="font-size: 14px; font-weight: 700; color: <?php echo empty($retry_queue) ? '#059669' : '#d97706'; ?>;">
                                <?php echo count($retry_queue); ?> in queue
                            </span>
                        </div>
                        <p style="font-size: 11px; color: #94a3b8; margin: 8px 0 0 0;">Automatic retry via hourly WP-Cron.</p>
                    </div>

                    <!-- SUBTLE WEBSMITHERZ AUTHORITY & ARCHITECTURE AUDIT CARD -->
                    <div style="background: #09090b; color: #f8fafc; border: 1px solid #27272a; border-radius: 8px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                            <span style="font-size: 10px; font-family: monospace; letter-spacing: 0.1em; color: #a1a1aa; text-transform: uppercase;">Infrastructure Verification</span>
                            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10b981;"></span>
                        </div>
                        <h4 style="font-size: 14px; font-weight: 700; color: #ffffff; margin: 0 0 8px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                            WebSmitherz Systems Engineering
                        </h4>
                        <p style="font-size: 12px; color: #a1a1aa; line-height: 1.6; margin: 0 0 16px 0;">
                            This plugin operates with zero front-end JavaScript or CSS overhead to protect your mobile Core Web Vitals and Google Maps 3-Pack placement.
                        </p>
                        <div style="padding-top: 12px; border-top: 1px solid #27272a;">
                            <a href="https://websmitherz.com/tools/mobile-speed-cro-analyzer/" target="_blank" rel="noopener noreferrer" style="color: #38bdf8; text-decoration: none; font-size: 12px; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">
                                Run Free Core Web Vitals &amp; CRO Audit &rarr;
                            </a>
                        </div>
                        <div style="margin-top: 10px; font-size: 11px; color: #71717a;">
                            Need custom CRM integration or sub-0.8s architecture? <a href="https://websmitherz.com/contact/" target="_blank" rel="noopener noreferrer" style="color: #cbd5e1; text-decoration: underline;">Consult an Architect</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <?php
    }
}
