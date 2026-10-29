# Deploying a client site — step by step

Internal guide for Data Master. Follow it top to bottom every time you put a template live on a
client's domain. It starts from nothing: no mailbox, no DNS records, no files on the server.

**Time needed:** about 45 minutes the first time, 15–20 minutes once you know it.

> Menu names below follow Plesk Obsidian as used by HappyByte. If a label looks slightly different
> in your panel, look for the closest match. The steps themselves don't change.

---

## Contents

0. [Before you start: collect these](#0-before-you-start-collect-these)
1. [Prepare the site files on your Mac](#1-prepare-the-site-files-on-your-mac)
2. [Add the domain in Plesk and switch on SSL](#2-add-the-domain-in-plesk-and-switch-on-ssl)
3. [Find out where the client's email lives](#3-find-out-where-the-clients-email-lives)
4. [Create the noreply mailbox](#4-create-the-noreply-mailbox)
5. [Set up SPF, DKIM and DMARC](#5-set-up-spf-dkim-and-dmarc)
6. [Set the PHP version](#6-set-the-php-version)
7. [Upload the website](#7-upload-the-website)
8. [Create the contact form config](#8-create-the-contact-form-config)
9. [Test everything](#9-test-everything)
10. [Hand over and record](#10-hand-over-and-record)
- [Troubleshooting](#troubleshooting)
- [Later changes](#later-changes)

---

## 0. Before you start: collect these

Fill this in before touching the server. You need every line.

| Item | Example | Notes |
|---|---|---|
| Client's domain | `clientdomain.gr` | Registered and paid by the client |
| Main address (www or not) | `https://www.clientdomain.gr` | Pick one; the other will redirect to it |
| Address that receives form messages | `info@clientdomain.gr` | One or more. Must be an inbox someone actually reads |
| Where that inbox is hosted | HappyByte / Google Workspace / Microsoft 365 / other | Decides step 4 (see step 3) |
| Where the domain's DNS is managed | Plesk (HappyByte) / the registrar (e.g. Papaki, Top.Host) | Decides where you add records in step 5 |
| Business details for the privacy page | Name, ΑΦΜ, ΓΕΜΗ, address, phone, email | For `legal/sites.json` |
| Template chosen | `dental` | Folder name under `websites/` |

---

## 1. Prepare the site files on your Mac

1. Open your local copy of this repo and pull the latest version:

   ```bash
   cd ~/datamaster/github/website_templates
   git pull
   ```

2. Copy the chosen template to a working folder **outside** the repo (client files never go into
   this public repo):

   ```bash
   mkdir -p ~/datamaster/clients/clientdomain.gr
   cp -R websites/dental/. ~/datamaster/clients/clientdomain.gr/site/
   ```

3. In `site/index.html`:
   - replace the sample texts, phone numbers, emails, addresses, photos and business name with
     the client's;
   - **remove the demo ribbon** at the top (the bar that says "Demo template by Data Master");
   - update the `<title>`, the meta description and the schema.org block in `<head>`.

4. Privacy page: add the client to `legal/sites.json` (copy the template's entry, fill in the
   business details, set the `uses_…` flags to what the site really uses), then build it and copy
   the result into the client folder. See [`legal/README.md`](legal/README.md).

   ```bash
   python3 legal/build.py <entry-name>
   ```

5. Make sure the folder `site/dm-contact/` is there (it comes with every template) and contains
   `contact.php`, `contact-form.js`, `.htaccess` and `lib/`.
   `.htaccess` is a hidden file. In Finder press **Cmd + Shift + .** to see it.

6. Open `site/index.html` in your browser and click through it. The form will show its thank-you
   message without sending anything; that's demo mode, which is normal on your Mac.

---

## 2. Add the domain in Plesk and switch on SSL

1. Log in to Plesk (HappyByte).
2. **Websites & Domains → Add Domain**, enter `clientdomain.gr`, keep the document root as
   `httpdocs`.
3. If the domain's DNS is at the registrar, point it to HappyByte now:
   - `A` record for `@` and for `www` → the server IP shown in Plesk;
   - wait until `https://clientdomain.gr` reaches the Plesk default page (minutes to a few hours).
4. **SSL/TLS Certificates → Install a free basic certificate (Let's Encrypt)** and tick:
   - the domain **and** `www`;
   - **Secure webmail** / the **mail** subdomain;
   - then **Assign the certificate to mail domain** (wording varies: "Secure mail"), so
     `mail.clientdomain.gr` has a valid certificate. The contact form logs in to the mail
     server through that name in step 8.
5. **Hosting Settings**: turn on **Permanent SEO-safe 301 redirect from HTTP to HTTPS**, and set the
   preferred domain (`www.clientdomain.gr` or `clientdomain.gr`) to match step 0.

---

## 3. Find out where the client's email lives

Look up the domain's MX records (Plesk **DNS Settings**, the registrar's DNS page, or
[mxtoolbox.com/MXLookup](https://mxtoolbox.com/MXLookup.aspx)):

| MX points to | Case | What you do in step 4 |
|---|---|---|
| `mail.clientdomain.gr` / the HappyByte server | **A: email on HappyByte** | Create `noreply@clientdomain.gr` in Plesk (4A) |
| `aspmx.l.google.com`, `smtp.google.com` | **B: Google Workspace** | Don't create mail for the main domain in Plesk (4B) |
| `*.mail.protection.outlook.com` | **B: Microsoft 365** | Same as Google (4B) |
| Anything else (registrar mail, Zoho…) | **B** | Same as Google (4B) |
| No MX record / new domain | Ask the client where they want their email. If on HappyByte → **A** | |

> **Why this matters:** if the client's email is with Google or Microsoft and you create a mailbox
> for the *same domain* in Plesk, the server starts believing it handles that domain's mail. Form
> messages to `info@clientdomain.gr` then stay on the HappyByte server, or bounce, and never reach
> Google/Microsoft. The form looks fine and the client never gets a single message.

---

## 4. Create the noreply mailbox

### 4A. Client email on HappyByte (most common)

1. **Websites & Domains → clientdomain.gr → Mail → Create Email Address**.
2. Email address: `noreply`.
3. Password: click **Generate** and copy it somewhere safe right away. You'll need it in step 8.
4. **Untick** "Can be used to log in to Plesk".
5. Mailbox size: set a small quota (e.g. 50 MB). This mailbox only sends, it never receives real
   mail.
6. Save.
7. Make sure the receiving address (`info@clientdomain.gr`) also exists and that someone can read
   it (webmail or their phone).

### 4B. Client email on Google Workspace / Microsoft 365 / elsewhere

Pick one:

- **Option 1 (recommended): a sending subdomain on HappyByte.**
  1. **Websites & Domains → Add Subdomain** → `mail-out.clientdomain.gr`
     (any name that isn't `www` or `mail`).
  2. On that subdomain: **Mail → Create Email Address** → `noreply@mail-out.clientdomain.gr`,
     generated password, not allowed to log in to Plesk, small quota.
  3. In step 5, the SPF/DKIM/DMARC records go on `mail-out.clientdomain.gr`, not on the main domain.
  4. The client's own mail on the main domain is never touched.

- **Option 2: the mailbox at the client's provider.**
  Ask the client (or their IT) to create `noreply@clientdomain.gr` at Google/Microsoft and give you
  SMTP details. Google needs an **app password** with 2-step verification
  (`smtp.gmail.com`, port 465). Microsoft 365 often has SMTP sign-in switched off and is moving
  away from it, so prefer Option 1 there.

---

## 5. Set up SPF, DKIM and DMARC

These three DNS records tell Gmail, Outlook etc. that the server is allowed to send for the domain.
Without them, form messages land in spam.

First check where DNS is managed (step 0):
- **Plesk manages DNS** → Plesk creates SPF and DKIM itself; you only check them.
- **The registrar manages DNS** → you copy the records from Plesk into the registrar's DNS page.

### DKIM

1. **Mail → Mail Settings** (tab), select the domain (or the `mail-out` subdomain for 4B),
   tick **Use DKIM spam protection system to sign outgoing email messages**, save.
2. If DNS is at the registrar: go to Plesk **DNS Settings** for the domain, find the TXT record
   named `default._domainkey` and create the same TXT record at the registrar.

### SPF

1. In Plesk **DNS Settings**, find the TXT record starting with `v=spf1`.
2. If DNS is at the registrar, create it there too.
3. **Only one SPF record per domain.** If one already exists (e.g. for Google), *merge* them instead
   of adding a second:

   | Case | SPF record |
   |---|---|
   | A: everything on HappyByte | the one Plesk generates, e.g. `v=spf1 +a +mx -all` |
   | 4B Option 1 (subdomain) | on `mail-out.clientdomain.gr`: `v=spf1 +a +mx -all`, main domain untouched |
   | Google + HappyByte sending from the main domain | `v=spf1 include:_spf.google.com a:<HappyByte server host name> ~all` |

### DMARC

Add a TXT record (Plesk **DNS Settings → Add Record**, or at the registrar):

| Host / name | Type | Value |
|---|---|---|
| `_dmarc` (for 4B Option 1: `_dmarc.mail-out`) | TXT | `v=DMARC1; p=none;` |

Start with `p=none`. After a month with no problems you can tighten it to `p=quarantine`.

### Check

DNS changes can take up to a few hours. Check with
[mxtoolbox.com/SuperTool](https://mxtoolbox.com/SuperTool.aspx): `spf:clientdomain.gr`,
`dkim:clientdomain.gr:default`, `dmarc:clientdomain.gr`. All three should be found without errors.

---

## 6. Set the PHP version

**Websites & Domains → clientdomain.gr → PHP** (or **PHP Settings**) → choose **PHP 8.1 or newer**
(8.3 if offered), handler **FPM**. Save.

---

## 7. Upload the website

1. **Websites & Domains → clientdomain.gr → File Manager**. You're in the domain's home folder: you
   see `httpdocs` and a few system folders.
2. Open `httpdocs`, delete Plesk's default `index.html` and other placeholder files.
3. Upload everything from your `site/` folder: `index.html`, `privacy.html`, images, and the whole
   `dm-contact/` folder **including `.htaccess`**. File Manager uploads single files; for folders
   either upload a `.zip` and use **Extract Files**, or use FTP (Cyberduck / FileZilla with the
   FTP account from **Websites & Domains → FTP Access**).

   The result in `httpdocs/` should be:

   ```
   httpdocs/
   ├── index.html
   ├── privacy.html
   └── dm-contact/
       ├── .htaccess
       ├── contact.php
       ├── contact-form.js
       └── lib/PHPMailer/ (Exception.php, PHPMailer.php, SMTP.php, LICENSE)
   ```

4. Open `https://www.clientdomain.gr`. The site loads, with the padlock.

---

## 8. Create the contact form config

The config holds the noreply password, so it goes **outside** `httpdocs`, where it can never be
downloaded.

1. On your Mac, copy [`contact-kit/dm-contact-config.sample.php`](contact-kit/dm-contact-config.sample.php)
   to a new file named exactly **`dm-contact-config.php`** (in the client folder, not in the repo).
2. Fill it in:

   | Setting | What to put | Example |
   |---|---|---|
   | `site_name` | Business name as it should appear in the sender name | `Παπαδάκης & Συνεργάτες` |
   | `site_url` | The main address from step 0, with `https://` | `https://www.clientdomain.gr` |
   | `to` | Who receives the messages | `['info@clientdomain.gr']` |
   | `from_email` | The noreply address from step 4 | `noreply@clientdomain.gr` (4B: `noreply@mail-out.clientdomain.gr`) |
   | `transport` | Leave `smtp` | `smtp` |
   | `smtp_host` | `mail.` + the client's domain (4A), or the server's host name (4B Option 1) | `mail.clientdomain.gr` |
   | `smtp_port` / `smtp_secure` | Leave `465` / `ssl` | |
   | `smtp_pass` | The password from step 4 | |
   | `required` | Leave `['name', 'consent']` (every template has these fields) | |
   | `secret` | Any random string (e.g. generate a password) | |

   If you get certificate errors in step 9, set `smtp_host` to the server's own host name (shown in
   Plesk under **Tools & Settings** or in HappyByte's welcome email). Use
   `'smtp_verify_peer' => false` only as a last resort, and only with a host on the same server.

3. In **File Manager**, go to the domain's **home folder** (one level *above* `httpdocs`, the folder
   where you see `httpdocs` itself) and upload `dm-contact-config.php` there.

   ```
   (domain home)/
   ├── dm-contact-config.php     ← here
   └── httpdocs/
       └── dm-contact/ ...
   ```

   The script also creates a folder `dm-contact-storage/` here by itself for its anti-flood counter.
   That's expected.

   *If the panel doesn't let you upload outside `httpdocs`:* name the file `config.php` and put it in
   `httpdocs/dm-contact/` instead. The `.htaccess` there blocks it from the web.

---

## 9. Test everything

Do every check. Sending one message that "seems to work" isn't enough.

| # | Test | Expected |
|---|---|---|
| 1 | Open the site on your phone and on a computer | Loads with the padlock, no demo ribbon |
| 2 | Send the form with your own details, using a Gmail address as the visitor email | "Thank you…" message on the page |
| 3 | Check the client's inbox (`info@…`) | Message arrives within a minute, **in the inbox, not spam**. From: "Φόρμα επικοινωνίας – *Business name*" |
| 4 | Click **Reply** in that email | The reply goes to the Gmail address you typed, not to noreply |
| 5 | Switch the page to English (bilingual templates) and send again | Arrives, marked "Γλώσσα σελίδας: EN" |
| 6 | Deliverability score: in the config temporarily set `'to' => ['<address from mail-tester.com>']`, send the form, open the mail-tester result, then put the real address back | Score **9/10 or higher**. Below that, mail-tester tells you what's missing (usually SPF/DKIM) |
| 7 | Open `https://www.clientdomain.gr/dm-contact/lib/PHPMailer/PHPMailer.php` | 403 or 404 (blocked) |
| 8 | Open `https://www.clientdomain.gr/dm-contact/contact.php` directly | A short "Μη επιτρεπτό αίτημα" page (405). That's correct: it only accepts form posts |
| 9 | Open `https://www.clientdomain.gr/dm-contact-config.php` | 404 (it's outside the website) |

If anything fails, see [Troubleshooting](#troubleshooting).

---

## 10. Hand over and record

1. Save in your password manager, under the client's name: the noreply address and password, the
   SMTP host, and where DNS is managed.
2. Keep the client folder (`~/datamaster/clients/clientdomain.gr/`) with the final `site/` and the
   config. Don't commit it to this public repo.
3. Tell the client:
   - form messages arrive at `info@…` from "Φόρμα επικοινωνίας – …";
   - they reply with the normal **Reply** button;
   - they should **not delete or change** the `noreply@` mailbox. If they want messages to go to a
     different address, they ask you.
4. Make sure the contract/terms include the data-processing (DPA) clause: messages pass through
   your hosting.

---

## Troubleshooting

Server errors from the form are written to the domain's log: **Websites & Domains → clientdomain.gr
→ Logs**, search for `dm-contact`. Visitors never see technical details.

| Symptom | Likely cause | Fix |
|---|---|---|
| Page says "Δεν ήταν δυνατή η αποστολή…" and the log shows `Could not authenticate` | Wrong noreply password, or `smtp_user` differs from the mailbox | Re-check `smtp_pass`. Reset the mailbox password in Plesk and update the config |
| Log shows `SMTP connect() failed` or certificate errors | `smtp_host` has no valid certificate, or port blocked | Use the server host name as `smtp_host` (step 8); check step 2.4; try port `587` with `'smtp_secure' => 'tls'` |
| "Thank you" appears but nothing arrives, nothing in the log | Email delivered locally on the server instead of to Google/Microsoft (step 3), or in spam | Check spam first. Then check MX: if mail is with Google/Microsoft, use step 4B |
| Messages arrive in spam | SPF/DKIM/DMARC missing or wrong | Redo step 5, then test 6 (mail-tester) |
| Page says "Μη επιτρεπτό αίτημα" (Request not allowed) when sending | `site_url` doesn't match the address in the browser (www vs non-www, http vs https) | Fix `site_url`, or add both under `'allowed_origins' => ['https://clientdomain.gr', 'https://www.clientdomain.gr']` |
| Page says "Έχετε στείλει αρκετά μηνύματα…" | Anti-flood: 5 messages per visitor per 10 minutes | Normal while testing. Wait 10 min, or delete `dm-contact-storage/rate.json` |
| Blank page / error 500 when sending | PHP older than 8.1, or the config is missing or has a typo | Step 6; check that `dm-contact-config.php` is in the right folder; open it and check for a missing comma or quote |
| Form shows "thank you" but never sends on the live site | The site is in demo mode: `contact-form.js` thinks it isn't live | Check the form tag has `action="dm-contact/contact.php"` and the site isn't opened as a local file |
| The form doesn't react at all | `contact-form.js` not uploaded, or the `<script src="dm-contact/contact-form.js">` line was removed | Re-upload `dm-contact/`; check the line before `</body>` |
| Owner sees field names in English | The visitor used the English version of the page | Intended. Labels follow the visitor's language. To force Greek: `'labels' => ['need' => 'Τι χρειάζεται']` in the config |

---

## Later changes

| Change | How |
|---|---|
| Messages to a different / extra address | Edit `to` in `dm-contact-config.php` on the server |
| Rotate the noreply password | Plesk → Mail → noreply → change password → update `smtp_pass` |
| A fix or improvement to the form code | Edit **only** `contact-kit/dm-contact/` in this repo, run `./tools/sync-contact-kit.sh` to copy it into every template, commit, then re-upload `dm-contact/` to each live site |
| Turn on a stricter DMARC | After a month without issues, change `p=none` → `p=quarantine` |

How the pieces fit together and what each setting does: see [`contact-kit/README.md`](contact-kit/README.md).
