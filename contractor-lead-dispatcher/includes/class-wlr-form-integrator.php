<?php
/**
 * Universal Form Builders Interceptor
 * Integrates hooks for Elementor Pro, CF7, WPForms, Gravity Forms, and Formidable
 */

if (!defined('ABSPATH')) {
    exit;
}

class WLR_Form_Integrator {

    public static function init() {
        // 1. Elementor Pro Forms
        add_action('elementor_pro/forms/new_record', array(__CLASS__, 'handle_elementor_pro_form'), 10, 2);

        // 2. Contact Form 7
        add_action('wpcf7_mail_sent', array(__CLASS__, 'handle_cf7_form'), 10, 1);

        // 3. WPForms
        add_action('wpforms_process_complete', array(__CLASS__, 'handle_wpforms_form'), 10, 4);

        // 4. Gravity Forms
        add_action('gform_after_submission', array(__CLASS__, 'handle_gravity_form'), 10, 2);

        // 5. Formidable Forms
        add_action('frm_after_create_entry', array(__CLASS__, 'handle_formidable_form'), 10, 2);
    }

    /**
     * Intercept Elementor Pro Form submissions
     */
    public static function handle_elementor_pro_form($record, $handler) {
        $raw_fields = $record->get('fields');
        $lead_data = array();

        foreach ($raw_fields as $id => $field) {
            $key = !empty($field['title']) ? sanitize_key($field['title']) : $id;
            $lead_data[$key] = $field['value'];
        }

        $form_name = $record->get_form_settings('form_name');
        $source = !empty($form_name) ? 'Elementor Pro (' . $form_name . ')' : 'Elementor Pro Form';

        WLR_Dispatcher::dispatch($lead_data, $source);
    }

    /**
     * Intercept Contact Form 7 submissions
     */
    public static function handle_cf7_form($contact_form) {
        $submission = WPCF7_Submission::get_instance();
        if (!$submission) {
            return;
        }

        $posted_data = $submission->get_posted_data();
        $lead_data = array();

        foreach ($posted_data as $key => $value) {
            if (strpos($key, '_wpcf7') === 0) {
                continue; // skip internal CF7 meta fields
            }
            $lead_data[sanitize_key($key)] = $value;
        }

        $title = $contact_form->title();
        $source = !empty($title) ? 'Contact Form 7 (' . $title . ')' : 'Contact Form 7';

        WLR_Dispatcher::dispatch($lead_data, $source);
    }

    /**
     * Intercept WPForms submissions
     */
    public static function handle_wpforms_form($fields, $entry, $form_data, $entry_id) {
        $lead_data = array();

        foreach ($fields as $field) {
            $key = !empty($field['name']) ? sanitize_key($field['name']) : 'field_' . $field['id'];
            $lead_data[$key] = $field['value'];
        }

        $form_title = isset($form_data['settings']['form_title']) ? $form_data['settings']['form_title'] : 'WPForms';
        $source = 'WPForms (' . $form_title . ')';

        WLR_Dispatcher::dispatch($lead_data, $source);
    }

    /**
     * Intercept Gravity Forms submissions
     */
    public static function handle_gravity_form($entry, $form) {
        $lead_data = array();

        foreach ($form['fields'] as $field) {
            $key = !empty($field->label) ? sanitize_key($field->label) : 'input_' . $field->id;
            $val = rgar($entry, (string) $field->id);
            if (!empty($val)) {
                $lead_data[$key] = $val;
            }
        }

        $source = 'Gravity Forms (' . $form['title'] . ')';
        WLR_Dispatcher::dispatch($lead_data, $source);
    }

    /**
     * Intercept Formidable Forms submissions
     */
    public static function handle_formidable_form($entry_id, $form_id) {
        if (!class_exists('FrmEntry')) {
            return;
        }

        $entry = FrmEntry::getOne($entry_id, true);
        if (!$entry || empty($entry->metas)) {
            return;
        }

        $lead_data = array();
        foreach ($entry->metas as $field_id => $val) {
            $field = FrmField::getOne($field_id);
            $key = $field ? sanitize_key($field->name) : 'field_' . $field_id;
            $lead_data[$key] = $val;
        }

        $source = 'Formidable Forms (ID ' . $form_id . ')';
        WLR_Dispatcher::dispatch($lead_data, $source);
    }
}
