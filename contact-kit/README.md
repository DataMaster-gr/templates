# Contact form kit

Makes a template's contact form send a real email to the site owner.
No database and no third-party service: PHP 8.1+ on the client's hosting (Plesk / HappyByte).

**Deploying a site?** Follow the step-by-step guide: [`../DEPLOY.md`](../DEPLOY.md).

```
contact-kit/
├── dm-contact/                    ← master copy; every template has an identical copy
│   ├── contact.php                  receives the form and sends the email (same on every site)
│   ├── contact-form.js              sends the form without leaving the page; demo mode on GitHub Pages
│   ├── .htaccess                    blocks web access to everything except contact.php
│   └── lib/PHPMailer/               standard mail library (PHPMailer 6.12, LGPL)
└── dm-contact-config.sample.php   ← the only per-client file (copy, rename, fill in)
```

Edit the code **only here**, then run `../tools/sync-contact-kit.sh` to copy it into all templates.

## How it works

1. The visitor fills in the form. `contact-form.js` sends it to `dm-contact/contact.php` in the
   background, together with the labels the visitor saw and the page language.
2. `contact.php` checks it (spam traps, origin, required fields, rate limit), logs in to the
   client's `noreply@` mailbox over SMTP and emails the owner.
3. The visitor sees the template's thank-you message, or a clear error in Greek / English.

On GitHub Pages and when opened as a local file, `contact-form.js` stays in **demo mode**: it shows
the thank-you message and sends nothing. The templates in this repo are therefore both the live
demos and production-ready.

## What the owner receives

```
From:     Φόρμα επικοινωνίας – Παπαδάκης & Συνεργάτες <noreply@clientdomain.gr>
Reply-To: Μαρία Κωνσταντίνου <maria@example.com>
Subject:  Νέο μήνυμα από την ιστοσελίδα – Μαρία Κωνσταντίνου
```

A table with every field (dropdowns and radio buttons as the text the visitor saw), the date
(Athens time), the page language and a link to the page. "Reply" writes straight to the visitor.

## Wiring a form (already done in all six templates)

```html
<form action="dm-contact/contact.php" method="post" data-dm-contact
      data-sent-target="#formCard" novalidate>
  ...
</form>
...
<script src="dm-contact/contact-form.js" defer></script>
</body>
```

- `data-sent-target` (optional): the element that gets class `sent` on success, which shows the
  template's own thank-you box. Without it, the thank-you text appears under the button.
- `data-dm-contact="demo"` forces demo mode anywhere.
- Fields with special handling: `name`, `email` (becomes Reply-To), `phone`, `message`,
  `description`, `consent`. Every other field is included as is.

## Protection built in

| Threat | What happens |
|---|---|
| Bots filling every field | Hidden honeypot field → silently "accepted", nothing sent |
| Bots submitting instantly | Under 3 seconds after page load → silently "accepted", nothing sent |
| Posting from another website | Refused: only the site's own domain is accepted |
| Flooding | Max 5 messages per visitor per 10 minutes (IP stored hashed, auto-expires) |
| Email header injection | Addresses validated by PHPMailer; the recipient comes only from the config |
| Wrong or changed SMTP password | Visitor sees "try again or call us"; the error goes to the server log |

Nothing is stored except the rate-limit file (hashed IPs, kept 10 minutes) in
`dm-contact-storage/`, next to `httpdocs`.

## All config settings

See the comments in [`dm-contact-config.sample.php`](dm-contact-config.sample.php). Optional ones:

| Setting | Default | Use |
|---|---|---|
| `from_name` | `Φόρμα επικοινωνίας – <site_name>` | Different sender name |
| `subject` | `Νέο μήνυμα από την ιστοσελίδα – <visitor>` | Fixed subject |
| `labels` | labels from the form | Force field labels in the owner's email |
| `allowed_origins` | `site_url` with and without `www` | Extra domains that may post (e.g. during a domain move) |
| `thanks_url` | none | Thank-you page for visitors without JavaScript |
| `transport` | `smtp` | `mail` = server's own mail system, no password; only if the domain's email is on the same server |
| `smtp_verify_peer` | `true` | `false` only for a same-server host with a certificate mismatch |
| `rate_limit` / `rate_window` | `5` / `600` | Anti-flood limits |
| `min_seconds` | `3` | Time trap |
| `storage_dir` | `../dm-contact-storage` (next to `httpdocs`) | Where the rate-limit file goes |
| `debug` | `false` | More detail in the server log |
