<?php
/**
 * Data Master — contact form mailer
 *
 * Receives a website contact form and emails it to the site owner.
 * No database. The only per-site file is the config (see config.sample.php).
 *
 * Same file on every site: do not edit, change the config instead.
 */

declare(strict_types=1);

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception as MailException;

require __DIR__ . '/lib/PHPMailer/Exception.php';
require __DIR__ . '/lib/PHPMailer/PHPMailer.php';
require __DIR__ . '/lib/PHPMailer/SMTP.php';

/* ------------------------------------------------------------------ */
/* Config                                                              */
/* ------------------------------------------------------------------ */

// Preferred: config outside the public folder (Plesk: next to httpdocs, not inside it).
// This file lives in  httpdocs/dm-contact/ , so two levels up is the private folder.
$configPaths = [
    dirname(__DIR__, 2) . '/dm-contact-config.php',
    __DIR__ . '/config.php',
];
$cfg = null;
foreach ($configPaths as $p) {
    if (is_file($p)) { $cfg = require $p; break; }
}
if (!is_array($cfg)) {
    http_response_code(500);
    error_log('[dm-contact] config file not found');
    exit('Configuration missing.');
}

$cfg += [
    'site_name'        => '',
    'site_url'         => '',
    'to'               => [],
    'from_email'       => '',
    'from_name'        => null,
    'subject'          => null,
    'transport'        => 'smtp',     // 'smtp' or 'mail' (local server sending)
    'smtp_host'        => 'localhost',
    'smtp_port'        => 465,
    'smtp_secure'      => 'ssl',      // 'ssl' (465), 'tls' (587) or '' (none)
    'smtp_user'        => null,       // defaults to from_email
    'smtp_pass'        => '',
    'smtp_verify_peer' => true,
    'allowed_origins'  => [],         // defaults to site_url (+ www/non-www)
    'required'         => ['name'],
    'require_contact'  => true,       // at least one of email / phone
    'labels'           => [],
    'thanks_url'       => null,
    'rate_limit'       => 5,          // messages per IP...
    'rate_window'      => 600,        // ...per this many seconds
    'min_seconds'      => 3,          // faster than this = bot
    'storage_dir'      => null,
    'secret'           => '',
    'debug'            => false,
];

/* ------------------------------------------------------------------ */
/* Texts                                                               */
/* ------------------------------------------------------------------ */

$lang = (isset($_POST['_lang']) && $_POST['_lang'] === 'en') ? 'en' : 'el';

$T = [
    'el' => [
        'ok'        => 'Ευχαριστούμε! Λάβαμε το μήνυμά σας και θα επικοινωνήσουμε μαζί σας σύντομα.',
        'invalid'   => 'Παρακαλούμε συμπληρώστε σωστά τα υποχρεωτικά πεδία.',
        'email'     => 'Η διεύθυνση email δεν φαίνεται σωστή.',
        'contact'   => 'Συμπληρώστε τηλέφωνο ή email για να επικοινωνήσουμε μαζί σας.',
        'consent'   => 'Χρειαζόμαστε τη συγκατάθεσή σας για να επικοινωνήσουμε μαζί σας.',
        'rate'      => 'Έχετε στείλει αρκετά μηνύματα. Δοκιμάστε ξανά σε λίγα λεπτά ή καλέστε μας.',
        'fail'      => 'Δεν ήταν δυνατή η αποστολή αυτή τη στιγμή. Δοκιμάστε ξανά ή καλέστε μας.',
        'forbidden' => 'Μη επιτρεπτό αίτημα.',
        'back'      => 'Επιστροφή στην ιστοσελίδα',
    ],
    'en' => [
        'ok'        => 'Thank you! We received your message and will get back to you shortly.',
        'invalid'   => 'Please fill in the required fields correctly.',
        'email'     => 'The email address does not look right.',
        'contact'   => 'Please leave a phone number or email so we can reach you.',
        'consent'   => 'We need your consent in order to contact you.',
        'rate'      => 'You have sent several messages already. Please try again in a few minutes or call us.',
        'fail'      => 'The message could not be sent right now. Please try again or call us.',
        'forbidden' => 'Request not allowed.',
        'back'      => 'Back to the website',
    ],
][$lang];

// Labels used in the email the owner receives (always Greek, the owner's language).
$defaultLabels = [
    'name'        => 'Ονοματεπώνυμο',
    'email'       => 'Email',
    'phone'       => 'Τηλέφωνο',
    'subject'     => 'Θέμα',
    'message'     => 'Μήνυμα',
    'description' => 'Περιγραφή',
    'consent'     => 'Συγκατάθεση επικοινωνίας',
];

/* ------------------------------------------------------------------ */
/* Helpers                                                             */
/* ------------------------------------------------------------------ */

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function respond(int $status, bool $ok, string $msg, array $cfg, array $T, bool $wantsJson, string $lang): never
{
    http_response_code($status);
    if ($wantsJson) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'message' => $msg], JSON_UNESCAPED_UNICODE);
        exit;
    }
    if ($ok && $cfg['thanks_url']) {
        header('Location: ' . $cfg['thanks_url'], true, 303);
        exit;
    }
    $back = $cfg['site_url'] ?: '/';
    header('Content-Type: text/html; charset=utf-8');
    echo '<!doctype html><html lang="' . $lang . '"><head><meta charset="utf-8">'
        . '<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
        . '<title>' . h($cfg['site_name']) . '</title>'
        . '<style>body{font-family:system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;margin:0;padding:16px;background:#f6f4f1;color:#1d1b19}'
        . 'main{max-width:460px;text-align:center}a{color:inherit;font-weight:600}</style></head><body><main>'
        . '<p>' . h($msg) . '</p><p><a href="' . h($back) . '">' . h($T['back']) . '</a></p></main></body></html>';
    exit;
}

function h(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function clean(mixed $v, int $max): string
{
    if (is_array($v)) { $v = implode(', ', array_map('strval', $v)); }
    $v = trim((string) $v);
    $v = preg_replace('/[^\P{C}\n\t]/u', '', $v) ?? '';   // drop control chars, keep newlines/tabs
    return mb_substr($v, 0, $max);
}

function oneLine(string $s): string
{
    return trim(preg_replace('/\s+/u', ' ', $s) ?? '');
}

function hostOf(string $url): string
{
    return strtolower((string) parse_url($url, PHP_URL_HOST));
}

$fail = fn (int $status, string $key) => respond($status, false, $T[$key], $cfg, $T, $wantsJson, $lang);
// Bots get a normal-looking success, so they learn nothing.
$fakeOk = fn () => respond(200, true, $T['ok'], $cfg, $T, $wantsJson, $lang);

/* ------------------------------------------------------------------ */
/* Request checks                                                      */
/* ------------------------------------------------------------------ */

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    $fail(405, 'forbidden');
}

// Only accept posts coming from this site's own pages.
$allowedHosts = array_map('hostOf', $cfg['allowed_origins']);
if (!$allowedHosts && $cfg['site_url']) {
    $hst = hostOf($cfg['site_url']);
    $bare = preg_replace('/^www\./', '', $hst);
    $allowedHosts = [$bare, 'www.' . $bare];
}
$origin = $_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '');
if ($allowedHosts && $origin !== '' && !in_array(hostOf($origin), $allowedHosts, true)) {
    $fail(403, 'forbidden');
}

// Honeypot: a hidden field real visitors never see.
if (trim((string) ($_POST['dm_hp'] ?? '')) !== '') {
    $fakeOk();
}

// Time trap: set by contact-form.js when the page loads. Missing = no JS, still allowed.
if (isset($_POST['_t']) && ctype_digit((string) $_POST['_t'])) {
    $elapsed = time() - intdiv((int) $_POST['_t'], 1000);
    if ($elapsed < (int) $cfg['min_seconds']) { $fakeOk(); }
}

/* ------------------------------------------------------------------ */
/* Collect and validate fields                                         */
/* ------------------------------------------------------------------ */

$reserved = ['dm_hp', '_t', '_lang', '_page', '_labels'];
$clientLabels = [];
if (!empty($_POST['_labels'])) {
    $decoded = json_decode((string) $_POST['_labels'], true);
    if (is_array($decoded)) {
        foreach ($decoded as $k => $v) {
            if (is_string($k) && is_string($v)) { $clientLabels[$k] = oneLine(clean($v, 120)); }
        }
    }
}

$fields = [];
foreach ($_POST as $key => $value) {
    if (in_array($key, $reserved, true) || !preg_match('/^[A-Za-z0-9_\-]{1,40}$/', (string) $key)) { continue; }
    if (count($fields) >= 30) { break; }
    $long = in_array($key, ['message', 'description'], true);
    $v = clean($value, $long ? 5000 : 300);
    if (!$long) { $v = oneLine($v); }
    if ($v !== '') { $fields[$key] = $v; }
}

if (in_array('consent', $cfg['required'], true) && empty($fields['consent'])) {
    $fail(422, 'consent');
}
foreach ($cfg['required'] as $req) {
    if (empty($fields[$req])) { $fail(422, 'invalid'); }
}

$email = $fields['email'] ?? '';
if ($email !== '' && !PHPMailer::validateAddress($email)) {
    $fail(422, 'email');
}
if ($cfg['require_contact'] && $email === '' && empty($fields['phone'])) {
    $fail(422, 'contact');
}

/* ------------------------------------------------------------------ */
/* Rate limit (per IP, stored hashed, no database)                     */
/* ------------------------------------------------------------------ */

$storage = $cfg['storage_dir'] ?: dirname(__DIR__, 2) . '/dm-contact-storage';
if (!is_dir($storage) && !@mkdir($storage, 0700, true)) {
    $storage = __DIR__ . '/storage';
    if (!is_dir($storage)) { @mkdir($storage, 0700, true); }
}
$rateFile = $storage . '/rate.json';
$ipHash = hash('sha256', ($cfg['secret'] ?: __DIR__) . '|' . ($_SERVER['REMOTE_ADDR'] ?? ''));
$now = time();

$fh = @fopen($rateFile, 'c+');
if ($fh) {
    flock($fh, LOCK_EX);
    $data = json_decode(stream_get_contents($fh) ?: '[]', true) ?: [];
    foreach ($data as $k => $stamps) {   // forget anything older than the window
        $data[$k] = array_values(array_filter($stamps, fn ($s) => $s > $now - (int) $cfg['rate_window']));
        if (!$data[$k]) { unset($data[$k]); }
    }
    $limited = count($data[$ipHash] ?? []) >= (int) $cfg['rate_limit'];
    if (!$limited) { $data[$ipHash][] = $now; }
    ftruncate($fh, 0);
    rewind($fh);
    fwrite($fh, json_encode($data));
    flock($fh, LOCK_UN);
    fclose($fh);
    if ($limited) { $fail(429, 'rate'); }
} elseif ($cfg['debug']) {
    error_log('[dm-contact] rate-limit storage not writable: ' . $storage);
}

/* ------------------------------------------------------------------ */
/* Build the email                                                     */
/* ------------------------------------------------------------------ */

$labelOf = function (string $key) use ($cfg, $clientLabels, $defaultLabels): string {
    if ($key === 'consent') {   // the checkbox text is a whole sentence; keep the email tidy
        return $cfg['labels'][$key] ?? $defaultLabels[$key];
    }
    return $cfg['labels'][$key]
        ?? $clientLabels[$key]
        ?? $defaultLabels[$key]
        ?? ucfirst(str_replace(['_', '-'], ' ', $key));
};

$page = (string) ($_POST['_page'] ?? '');
if ($page !== '' && (!preg_match('#^https?://#i', $page) || ($allowedHosts && !in_array(hostOf($page), $allowedHosts, true)))) {
    $page = '';
}

$when = (new DateTime('now', new DateTimeZone('Europe/Athens')))->format('d/m/Y H:i');
$siteName = $cfg['site_name'] ?: hostOf($cfg['site_url']);
$visitor = oneLine($fields['name'] ?? '');

$subject = $cfg['subject'] ?: 'Νέο μήνυμα από την ιστοσελίδα' . ($visitor !== '' ? ' – ' . $visitor : '');

$order = array_unique(array_merge(['name', 'phone', 'email'], array_keys($fields)));
$rows = [];
foreach ($order as $key) {
    if (!isset($fields[$key])) { continue; }
    $val = $fields[$key];
    if ($key === 'consent' || $val === 'on') { $val = 'Ναι'; }   // ticked checkboxes
    $rows[] = [$labelOf($key), $val];
}

$text = "Νέο μήνυμα από τη φόρμα επικοινωνίας του {$siteName}\n\n";
foreach ($rows as [$l, $v]) {
    $text .= str_contains($v, "\n") ? "{$l}:\n{$v}\n\n" : "{$l}: {$v}\n";
}
$text .= "\n—\nΗμερομηνία: {$when}\nΓλώσσα σελίδας: " . strtoupper($lang) . "\n";
if ($page !== '') { $text .= "Σελίδα: {$page}\n"; }
if ($email !== '') { $text .= "\nΑπαντήστε απευθείας σε αυτό το email για να γράψετε στον επισκέπτη.\n"; }

$html = '<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#1d1b19;max-width:600px">'
    . '<p style="margin:0 0 16px">Νέο μήνυμα από τη φόρμα επικοινωνίας του <strong>' . h($siteName) . '</strong></p>'
    . '<table cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%">';
foreach ($rows as [$l, $v]) {
    $html .= '<tr><td style="border-bottom:1px solid #e7e3dd;color:#6b655e;vertical-align:top;width:34%">' . h($l) . '</td>'
        . '<td style="border-bottom:1px solid #e7e3dd">' . nl2br(h($v)) . '</td></tr>';
}
$html .= '</table><p style="margin:16px 0 0;font-size:13px;color:#6b655e">Ημερομηνία: ' . h($when)
    . ' · Γλώσσα σελίδας: ' . strtoupper($lang)
    . ($page !== '' ? ' · <a href="' . h($page) . '" style="color:#6b655e">σελίδα</a>' : '') . '</p>'
    . ($email !== '' ? '<p style="font-size:13px;color:#6b655e">Απαντήστε απευθείας σε αυτό το email για να γράψετε στον επισκέπτη.</p>' : '')
    . '</div>';

/* ------------------------------------------------------------------ */
/* Send                                                                */
/* ------------------------------------------------------------------ */

$mail = new PHPMailer(true);
try {
    $mail->CharSet = PHPMailer::CHARSET_UTF8;
    $mail->Encoding = PHPMailer::ENCODING_BASE64;

    if ($cfg['transport'] === 'smtp') {
        $mail->isSMTP();
        $mail->Host = (string) $cfg['smtp_host'];
        $mail->Port = (int) $cfg['smtp_port'];
        $mail->SMTPAuth = true;
        $mail->Username = (string) ($cfg['smtp_user'] ?: $cfg['from_email']);
        $mail->Password = (string) $cfg['smtp_pass'];
        $mail->SMTPSecure = $cfg['smtp_secure'] === 'ssl' ? PHPMailer::ENCRYPTION_SMTPS
            : ($cfg['smtp_secure'] === 'tls' ? PHPMailer::ENCRYPTION_STARTTLS : '');
        $mail->SMTPAutoTLS = $cfg['smtp_secure'] !== '';
        if (!$cfg['smtp_verify_peer']) {
            $mail->SMTPOptions = ['ssl' => ['verify_peer' => false, 'verify_peer_name' => false, 'allow_self_signed' => true]];
        }
        $mail->Timeout = 15;
    } else {
        $mail->isMail();
        $mail->Sender = (string) $cfg['from_email'];   // envelope sender, for SPF/bounces
    }

    $mail->setFrom((string) $cfg['from_email'], (string) ($cfg['from_name'] ?? ('Φόρμα επικοινωνίας – ' . $siteName)));
    foreach ((array) $cfg['to'] as $to) { $mail->addAddress((string) $to); }
    if ($email !== '') { $mail->addReplyTo($email, $visitor); }

    $mail->Subject = $subject;
    $mail->isHTML(true);
    $mail->Body = $html;
    $mail->AltBody = $text;
    $mail->XMailer = ' ';   // don't advertise the library

    $mail->send();
} catch (MailException $e) {
    error_log('[dm-contact] send failed: ' . $mail->ErrorInfo);
    $fail(502, 'fail');
}

respond(200, true, $T['ok'], $cfg, $T, $wantsJson, $lang);
