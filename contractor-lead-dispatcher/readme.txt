=== Contractor Lead Dispatcher & Instant CRM Webhooks ===
Contributors: websmitherz, adrzzubairi
Donate link: https://websmitherz.com/
Tags: contractor leads, servicetitan, jobber, acculynx, webhook, lead dispatch, roofing, hvac, plumber
Requires at least: 5.6
Tested up to: 6.7
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Sub-60s webhook lead dispatcher for trade contractors. Automatically routes form submissions from Elementor, CF7, WPForms, and Gravity Forms directly to ServiceTitan, Jobber, AccuLynx, or custom endpoints with E.164 phone normalization and failover retry queues.

== Description ==

Trade contractors (Roofing, HVAC, Plumbing, Electrical, Remodeling) lose up to 74% of high-ticket reroof and replacement jobs when homeowner inquiries sit unread in an email inbox for hours.

**Contractor Lead Dispatcher** intercepts submissions from your existing WordPress forms and dispatches standardized, sanitized JSON payloads straight to your contractor CRM (ServiceTitan, Jobber, AccuLynx, HubSpot, GoHighLevel) or webhook middleware in under 60 seconds.

Built by the systems architects at [WebSmitherz](https://websmitherz.com/), this plugin introduces enterprise-grade failover logging and phone number normalization to WordPress without slowing down front-end page load speeds.

= Key Features =
* **Sub-60s Webhook Dispatch:** Sends form leads directly to trade CRM endpoints with non-blocking HTTP requests.
* **Broad Form Compatibility:** Native integration for Elementor Pro Forms, Contact Form 7, WPForms, Gravity Forms, and Formidable Forms.
* **E.164 Phone Normalization:** Automatically cleans up domestic and international phone numbers into standard format (`+1XXXXXXXXXX`) for instant SMS routing.
* **Resilient Failover Retry Queue:** Automatically retries failed webhook dispatches up to 3 times via WP-Cron if your CRM endpoint experiences temporary downtime.
* **Diagnostic Telemetry Log:** Visual log of the last 100 dispatches showing status codes, latency, and payload payloads without exposing sensitive API secrets.
* **Zero Front-End Bloat:** Completely headless on the front end. Adds zero CSS or JS to your public pages, preserving perfect 100 PageSpeed scores and sub-0.8s Core Web Vitals.
* **Developer Friendly:** Clean hooks (`wlr_before_dispatch`, `wlr_after_dispatch`) for advanced custom payload manipulation.

= Supported Form Builders =
1. Elementor Pro Form Widget
2. Contact Form 7
3. WPForms (Free & Pro)
4. Gravity Forms
5. Formidable Forms

== Installation ==

1. Upload the `contractor-lead-dispatcher` directory to `/wp-content/plugins/` or install directly via WordPress Plugin Directory.
2. Activate the plugin through the 'Plugins' menu in WordPress.
3. Navigate to **Lead Dispatcher** in your WordPress admin menu.
4. Paste your primary CRM webhook URL (e.g., ServiceTitan, Jobber, Zapier, Make, or custom CRM endpoint).
5. (Optional) Provide a secondary fallback webhook or shared secret header.
6. Submit a test form on your site and view the real-time delivery telemetry in your admin dashboard.

== Frequently Asked Questions ==

= Does this plugin require paid third-party services? =
No. The plugin connects directly to any HTTP/HTTPS webhook URL you specify. If your CRM supports webhooks or you use a middleware webhook endpoint, there are zero ongoing fees.

= Will this plugin slow down my website? =
Not at all. The plugin executes webhook requests asynchronously using WordPress's `wp_remote_post` during the form submission action. It injects zero scripts, zero styles, and zero tracking pixels into public front-end pages.

= What happens if our CRM is temporarily offline? =
The plugin includes an automatic local retry queue. If your CRM returns a 5xx error or connection timeout, the payload is scheduled for re-dispatch via WP-Cron.

= Can I use this for multiple forms simultaneously? =
Yes. The plugin listens globally to form submission hooks and automatically maps standard fields (Name, Email, Phone, Address, Scope, Service) into a clean, uniform payload.

== Screenshots ==

1. Diagnostic Telemetry Dashboard showing recent lead dispatches, response times, and payload status.
2. Webhook Settings panel with E.164 phone formatting and failover options.
3. Dispatch Health badge and system architecture status.

== Changelog ==

= 1.0.0 =
* Initial public release.
* Native hooks for Elementor Pro, CF7, WPForms, Gravity Forms, and Formidable Forms.
* E.164 phone number sanitation.
* WP-Cron failover retry queue.
* Diagnostic telemetry log table.
