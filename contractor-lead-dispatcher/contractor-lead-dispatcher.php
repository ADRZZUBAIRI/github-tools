<?php
/**
 * Plugin Name: Contractor Lead Dispatcher & Instant CRM Webhooks
 * Plugin URI: https://websmitherz.com/tools/contractor-lead-dispatcher/
 * Description: Sub-60s webhook lead dispatcher for trade contractors (Roofing, HVAC, Plumbing, Remodeling). Seamlessly intercepts submissions from Elementor, CF7, WPForms, and Gravity Forms and routes standardized JSON payloads directly to ServiceTitan, Jobber, AccuLynx, or custom endpoints with E.164 phone normalization and failover retry queues.
 * Version: 1.0.0
 * Author: WebSmitherz Systems Engineering
 * Author URI: https://websmitherz.com/
 * License: GPL-2.0+
 * License URI: http://www.gnu.org/licenses/gpl-2.0.txt
 * Text Domain: contractor-lead-dispatcher
 * Domain Path: /languages
 */

if (!defined('ABSPATH')) {
    exit;
}

define('WLR_VERSION', '1.0.0');
define('WLR_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('WLR_PLUGIN_URL', plugin_dir_url(__FILE__));
define('WLR_OPTION_SETTINGS', 'wlr_webhook_settings');
define('WLR_OPTION_LOGS', 'wlr_dispatch_telemetry');

// Autoload components
require_once WLR_PLUGIN_DIR . 'includes/class-wlr-sanitizer.php';
require_once WLR_PLUGIN_DIR . 'includes/class-wlr-dispatcher.php';
require_once WLR_PLUGIN_DIR . 'includes/class-wlr-form-integrator.php';

if (is_admin()) {
    require_once WLR_PLUGIN_DIR . 'admin/class-wlr-admin.php';
}

/**
 * Main Plugin Bootstrap Class
 */
class WebSmitherz_Lead_Router {
    private static $instance = null;

    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        // Register activation & cron hooks
        register_activation_hook(__FILE__, array($this, 'activate'));
        register_deactivation_hook(__FILE__, array($this, 'deactivate'));

        // Initialize cron retry worker
        add_action('wlr_cron_retry_dispatch', array($this, 'process_retry_queue'));

        // Bootstrap form interceptors
        WLR_Form_Integrator::init();

        // Admin initialization
        if (is_admin()) {
            WLR_Admin::init();
        }
    }

    public function activate() {
        // Set default settings if not exists
        if (!get_option(WLR_OPTION_SETTINGS)) {
            $defaults = array(
                'primary_webhook'   => '',
                'fallback_webhook'  => '',
                'auth_bearer_token' => '',
                'custom_headers'    => '',
                'normalize_phone'   => 1,
                'default_country'   => 'US',
                'retry_attempts'    => 3,
                'log_retention'     => 100
            );
            update_option(WLR_OPTION_SETTINGS, $defaults);
        }

        // Schedule cron worker if not already scheduled
        if (!wp_next_scheduled('wlr_cron_retry_dispatch')) {
            wp_schedule_event(time(), 'hourly', 'wlr_cron_retry_dispatch');
        }
    }

    public function deactivate() {
        $timestamp = wp_next_scheduled('wlr_cron_retry_dispatch');
        if ($timestamp) {
            wp_unschedule_event($timestamp, 'wlr_cron_retry_dispatch');
        }
    }

    public function process_retry_queue() {
        WLR_Dispatcher::process_retry_queue();
    }
}

add_action('plugins_loaded', array('WebSmitherz_Lead_Router', 'get_instance'));
