<?php
/**
 * Data Sanitization & Phone Normalization Helper
 */

if (!defined('ABSPATH')) {
    exit;
}

class WLR_Sanitizer {

    /**
     * Normalize telephone number into standard E.164 format (+1XXXXXXXXXX for North America)
     */
    public static function normalize_phone($raw_phone, $default_country = 'US') {
        if (empty($raw_phone)) {
            return '';
        }

        // Strip everything except digits and leading plus
        $cleaned = preg_replace('/[^\d+]/', '', trim($raw_phone));

        // If already starts with +, ensure proper length
        if (strpos($cleaned, '+') === 0) {
            $digits_only = substr($cleaned, 1);
            if (strlen($digits_only) >= 10 && strlen($digits_only) <= 15) {
                return '+' . $digits_only;
            }
        }

        // Domestic US/Canada normalization (10 or 11 digits)
        $digits = preg_replace('/\D/', '', $raw_phone);
        if ($default_country === 'US' || $default_country === 'CA') {
            if (strlen($digits) === 10) {
                return '+1' . $digits;
            }
            if (strlen($digits) === 11 && strpos($digits, '1') === 0) {
                return '+' . $digits;
            }
        }

        // Fallback: return cleaned digits with +
        return '+' . $digits;
    }

    /**
     * Recursively sanitize payload arrays
     */
    public static function sanitize_payload($data) {
        if (!is_array($data)) {
            return sanitize_text_field($data);
        }

        $sanitized = array();
        foreach ($data as $key => $value) {
            $clean_key = sanitize_key($key);
            if (is_array($value)) {
                $sanitized[$clean_key] = self::sanitize_payload($value);
            } else {
                if (is_email($value)) {
                    $sanitized[$clean_key] = sanitize_email($value);
                } else {
                    $sanitized[$clean_key] = sanitize_text_field($value);
                }
            }
        }
        return $sanitized;
    }
}
