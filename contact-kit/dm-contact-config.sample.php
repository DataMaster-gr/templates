<?php
/**
 * Per-site settings for contact.php — the ONLY file you change per client.
 *
 * Where to put it (first match wins):
 *   1. OUTSIDE the website, named  dm-contact-config.php
 *      Plesk: next to httpdocs, not inside it   ← recommended, never downloadable
 *   2. Inside httpdocs/dm-contact/, named  config.php   (blocked by .htaccess)
 *
 * Never commit the real file to git (it holds a password).
 */

return [
    // --- The site --------------------------------------------------------
    'site_name' => 'Παπαδάκης & Συνεργάτες',          // shown in the sender name
    'site_url'  => 'https://www.clientdomain.gr',      // forms from other sites are refused

    // --- Who receives the messages ----------------------------------------
    'to' => ['info@clientdomain.gr'],                  // one or more addresses

    // --- Who sends them (the per-client noreply mailbox) ------------------
    'from_email' => 'noreply@clientdomain.gr',
    // 'from_name' => 'Φόρμα επικοινωνίας – Παπαδάκης & Συνεργάτες',   // optional override

    // 'smtp' = log in to the noreply mailbox (default)
    // 'mail' = hand the message to the server's own mail system (no password needed;
    //          only when the domain's email is hosted on the same server)
    'transport'   => 'smtp',
    'smtp_host'   => 'mail.clientdomain.gr',           // a host name the server's certificate matches
    'smtp_port'   => 465,                              // 465 with 'ssl', or 587 with 'tls'
    'smtp_secure' => 'ssl',
    'smtp_pass'   => 'CHANGE-ME-long-random-password',
    // 'smtp_user' => 'noreply@clientdomain.gr',      // defaults to from_email

    // --- Form rules -------------------------------------------------------
    'required'        => ['name', 'consent'],          // field names that must be filled
    'require_contact' => true,                         // at least one of email / phone

    // Optional: nicer labels in the owner's email (otherwise taken from the form's own labels)
    // 'labels' => ['need' => 'Τι χρειάζεται', 'meeting' => 'Τρόπος συνάντησης'],

    // Optional: send visitors without JavaScript to a thank-you page
    // 'thanks_url' => 'https://www.clientdomain.gr/thank-you.html',

    // --- Protection -------------------------------------------------------
    'rate_limit'  => 5,        // max messages per visitor IP...
    'rate_window' => 600,      // ...per 10 minutes
    'secret'      => 'CHANGE-ME-random-string',        // used to hash visitor IPs

    'debug' => false,          // true = extra details in the server error log (never shown to visitors)
];
