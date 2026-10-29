#!/usr/bin/env python3
"""Build privacy.html («Πολιτική Απορρήτου & Cookies») for every template.

One shared text (Greek + English) lives in this file. Per-client facts and the
template's look come from legal/sites.json (compliance pack §9 variables).
Sections, table rows and cookies render only when the matching flag is on, so
each site lists exactly what it uses.

    python3 legal/build.py            # build all sites
    python3 legal/build.py dental     # build one site

Output: websites/<site>/privacy.html. Never hand-edit the output; change the
text here or the variables in sites.json and rebuild.

Not legal advice: the text must be reviewed once by a lawyer (pack §11).
"""
import datetime
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFIG = ROOT / "legal" / "sites.json"

MONTHS_EL = ["Ιανουαρίου", "Φεβρουαρίου", "Μαρτίου", "Απριλίου", "Μαΐου", "Ιουνίου",
             "Ιουλίου", "Αυγούστου", "Σεπτεμβρίου", "Οκτωβρίου", "Νοεμβρίου", "Δεκεμβρίου"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]


def esc(s):
    return html.escape(str(s), quote=True)


def tr(value, lang):
    """A config value is either a plain string or {"el": ..., "en": ...}."""
    if isinstance(value, dict):
        return value.get(lang) or value.get("el") or ""
    return value or ""


def months(n, lang):
    if lang == "el":
        return f"{n} {'μήνας' if n == 1 else 'μήνες'}"
    return f"{n} {'month' if n == 1 else 'months'}"


def fmt_date(iso, lang):
    d = datetime.date.fromisoformat(iso)
    if lang == "el":
        return f"{d.day} {MONTHS_EL[d.month - 1]} {d.year}"
    return f"{d.day} {MONTHS_EN[d.month - 1]} {d.year}"


def table(head, rows):
    th = "".join(f"<th scope=\"col\">{h}</th>" for h in head)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<div class=\"tbl\"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>"


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


# --------------------------------------------------------------------------
# Sector clauses (optional "sector" variable). Short, lawyer-review items.
# --------------------------------------------------------------------------
SECTOR = {
    "health": {
        "el": ("Δεδομένα υγείας και ιατρικό απόρρητο",
               "<p>Τα δεδομένα υγείας (ιστορικό, διαγνώσεις, θεραπείες) ανήκουν στις ειδικές κατηγορίες "
               "δεδομένων του άρθρου 9 ΓΚΠΔ. <strong>Δεν τα ζητάμε μέσω της ιστοσελίδας</strong>· παρακαλούμε "
               "μην τα αναγράφετε στη φόρμα ραντεβού. Θα τα συζητήσουμε στο ιατρείο.</p>"
               "<p>Όταν γίνετε ασθενής μας, ο ιατρικός σας φάκελος τηρείται στο ιατρείο για την παροχή "
               "υπηρεσιών υγείας (άρθρο 9 παρ. 2 στοιχ. η' ΓΚΠΔ), καλύπτεται από το ιατρικό απόρρητο και "
               "φυλάσσεται για όσο ορίζει ο Κώδικας Ιατρικής Δεοντολογίας (ν. 3418/2005). Η διαχείρισή του "
               "δεν γίνεται μέσω της ιστοσελίδας και δεν περιλαμβάνεται σε αυτή την πολιτική.</p>"),
        "en": ("Health data and medical confidentiality",
               "<p>Health data (history, diagnoses, treatments) is a special category of data under "
               "Article 9 GDPR. <strong>We do not ask for it through this website</strong>; please do not "
               "include it in the appointment form. We will discuss it at the practice.</p>"
               "<p>Once you become a patient, your medical record is kept at the practice for the provision "
               "of health care (Article 9(2)(h) GDPR), is covered by medical confidentiality and is retained "
               "for as long as the Greek Code of Medical Ethics (Law 3418/2005) requires. It is not handled "
               "through this website and is outside the scope of this policy.</p>"),
    },
    "law": {
        "el": ("Δικηγορικό απόρρητο",
               "<p>Ό,τι μας γνωστοποιείτε καλύπτεται από το δικηγορικό απόρρητο (Κώδικας Δικηγόρων, "
               "ν. 4194/2013). Η αποστολή της φόρμας <strong>δεν δημιουργεί σχέση εντολής</strong>. Μην "
               "αναφέρετε στη φόρμα ευαίσθητα στοιχεία ή λεπτομέρειες της υπόθεσης· θα τα συζητήσουμε "
               "προσωπικά.</p>"
               "<p>Πριν αναλάβουμε μια υπόθεση, ελέγχουμε για σύγκρουση συμφερόντων με βάση το όνομά σας και "
               "τα ονόματα των αντιδίκων (άρθρο 6 παρ. 1 στοιχ. γ' και στ' ΓΚΠΔ). Αν μας αναθέσετε την "
               "υπόθεση, τα στοιχεία σας τηρούνται στον φάκελο της υπόθεσης για όσο απαιτεί ο νόμος και η "
               "δεοντολογία.</p>"),
        "en": ("Legal professional privilege",
               "<p>Everything you share with us is protected by legal professional privilege (Greek Lawyers' "
               "Code, Law 4194/2013). Sending the form <strong>does not create a lawyer–client "
               "relationship</strong>. Please do not include sensitive details or the specifics of your case "
               "in the form; we will discuss them in person.</p>"
               "<p>Before taking on a matter we run a conflict-of-interest check using your name and the "
               "names of the other parties (Article 6(1)(c) and (f) GDPR). If you instruct us, your details "
               "are kept in the case file for as long as the law and our professional rules require.</p>"),
    },
    "accounting": {
        "el": ("Επαγγελματικό απόρρητο και πελάτες του γραφείου",
               "<p>Ό,τι μας γνωστοποιείτε καλύπτεται από το επαγγελματικό απόρρητο. Η φόρμα της ιστοσελίδας "
               "χρησιμοποιείται μόνο για να κλείσουμε μια πρώτη συνάντηση· μην αποστέλλετε μέσω αυτής "
               "κωδικούς Taxisnet, έγγραφα ή οικονομικά στοιχεία.</p>"
               "<p>Αν γίνετε πελάτης μας, τα στοιχεία σας επεξεργάζονται βάσει της σύμβασης συνεργασίας και "
               "τηρούνται για όσο ορίζει η φορολογική και λογιστική νομοθεσία.</p>"),
        "en": ("Professional confidentiality and clients of the firm",
               "<p>Everything you share with us is covered by professional confidentiality. The website form "
               "is only used to arrange a first meeting; please do not send Taxisnet passwords, documents or "
               "financial data through it.</p>"
               "<p>If you become a client, your data is processed under our engagement agreement and kept "
               "for as long as Greek tax and accounting law requires.</p>"),
    },
    "engineer": {
        "el": ("Στοιχεία έργων",
               "<p>Αν μας αναθέσετε μελέτη ή έργο, τα στοιχεία σας και τα στοιχεία του ακινήτου "
               "επεξεργάζονται βάσει της σύμβασης και τηρούνται για όσο απαιτεί η νομοθεσία για τις μελέτες, "
               "τις άδειες δόμησης και τη φορολογία.</p>"),
        "en": ("Project data",
               "<p>If you commission a study or project, your details and the property details are processed "
               "under our contract and kept for as long as the law on studies, building permits and tax "
               "requires.</p>"),
    },
    "courier": {
        "el": ("Δεδομένα αποστολών",
               "<p>Για την εκτέλεση μιας αποστολής επεξεργαζόμαστε τα στοιχεία αποστολέα και παραλήπτη "
               "(όνομα, διεύθυνση, τηλέφωνο) βάσει της σύμβασης μεταφοράς (άρθρο 6 παρ. 1 στοιχ. β' ΓΚΠΔ). "
               "Τα στοιχεία του παραλήπτη μάς τα δίνει ο αποστολέας. Τα αποστελλόμενα αντικείμενα "
               "καλύπτονται από το ταχυδρομικό απόρρητο και τα στοιχεία αποστολών τηρούνται για όσο ορίζουν "
               "η ταχυδρομική και η φορολογική νομοθεσία.</p>"),
        "en": ("Shipment data",
               "<p>To carry out a shipment we process the sender's and recipient's details (name, address, "
               "phone) under the transport contract (Article 6(1)(b) GDPR). The recipient's details are "
               "provided to us by the sender. Items are covered by postal secrecy, and shipment records are "
               "kept for as long as postal and tax law requires.</p>"),
    },
}


# --------------------------------------------------------------------------
# Page text
# --------------------------------------------------------------------------
UI = {
    "el": {
        "title": "Πολιτική Απορρήτου & Cookies",
        "updated": "Τελευταία ενημέρωση",
        "back": "Αρχική",
        "contents": "Περιεχόμενα",
        "settings": "Ρυθμίσεις cookies",
        "privacy": "Πολιτική Απορρήτου",
        "rights": "Όλα τα δικαιώματα διατηρούνται.",
        "demo_rib": "Demo πρότυπο από τη Data Master · Όλα τα στοιχεία είναι ενδεικτικά",
        "demo_link": "Όλα τα πρότυπα",
        "langs": "Γλώσσα",
    },
    "en": {
        "title": "Privacy & Cookie Policy",
        "updated": "Last updated",
        "back": "Home",
        "contents": "Contents",
        "settings": "Cookie settings",
        "privacy": "Privacy Policy",
        "rights": "All rights reserved.",
        "demo_rib": "Demo template by Data Master · All details are sample content",
        "demo_link": "All templates",
        "langs": "Language",
    },
}


def sections(c, lang):
    """Return [(id, heading, html)] for one language."""
    el = lang == "el"
    out = []
    name = esc(tr(c["business_name"], lang))
    title = esc(tr(c["trading_title"], lang))
    email = esc(c["email"])
    mail = f"<a href=\"mailto:{email}\">{email}</a>"
    form, book, ga, maps, news = (c["uses_contact_form"], c["uses_booking"], c["uses_ga4"],
                                  c["uses_maps"], c["uses_newsletter"])
    fm, bm, am = c["form_retention_months"], c["booking_retention_months"], c["analytics_retention_months"]

    # 1. Controller -------------------------------------------------------
    rows = [
        ("Επωνυμία" if el else "Business name", name),
        ("Διακριτικός τίτλος" if el else "Trading title", title),
        ("Διεύθυνση" if el else "Address", esc(tr(c["address"], lang))),
        ("ΑΦΜ" if el else "VAT no. (ΑΦΜ)", esc(c["afm"])),
    ]
    if c.get("gemi_number"):
        rows.append(("Αρ. ΓΕΜΗ" if el else "GEMI no.", esc(c["gemi_number"])))
    rows += [("Email", mail),
             ("Τηλέφωνο" if el else "Phone",
              f"<a href=\"tel:{esc(c['phone'].replace(' ', ''))}\">{esc(c['phone'])}</a>")]
    reg = c.get("profession_regulator")
    if reg:
        rows.append(("Επαγγελματικός φορέας" if el else "Professional body",
                     f"{esc(tr(reg['body'], lang))}, {'Α.Μ.' if el else 'reg. no.'} {esc(reg['licence'])}"))
    dl = "<dl class=\"facts\">" + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + "</dl>"
    intro = (f"<p>Υπεύθυνος επεξεργασίας των προσωπικών σας δεδομένων που συλλέγονται μέσω αυτής της "
             f"ιστοσελίδας είναι:</p>" if el else
             "<p>The controller of the personal data collected through this website is:</p>")
    out.append(("controller", "Υπεύθυνος επεξεργασίας" if el else "Data controller", intro + dl))

    # 2. What we collect --------------------------------------------------
    items = []
    if form:
        items.append("<strong>Φόρμα επικοινωνίας:</strong> όνομα, email, τηλέφωνο, μήνυμα." if el else
                     "<strong>Contact form:</strong> name, email, phone, message.")
    if book:
        items.append("<strong>Κράτηση ραντεβού:</strong> όνομα, τηλέφωνο, email και στοιχεία του ραντεβού "
                     "(ημερομηνία, ώρα, υπηρεσία, τυχόν σχόλιο)." if el else
                     "<strong>Appointment booking:</strong> name, phone, email and the appointment details "
                     "(date, time, service, any note).")
    if news:
        items.append("<strong>Newsletter:</strong> το email σας, μόνο αν εγγραφείτε." if el else
                     "<strong>Newsletter:</strong> your email address, only if you sign up.")
    items.append("<strong>Τεχνικά δεδομένα:</strong> διεύθυνση IP, τύπος συσκευής και φυλλομετρητή, ώρα "
                 "πρόσβασης, που καταγράφονται αυτόματα στα αρχεία καταγραφής (logs) του διακομιστή." if el else
                 "<strong>Technical data:</strong> IP address, device and browser type and time of access, "
                 "recorded automatically in the server logs.")
    if ga:
        items.append("<strong>Στατιστικά επισκεψιμότητας</strong> μέσω Google Analytics 4, "
                     "<strong>μόνο αν το αποδεχτείτε</strong> στις ρυθμίσεις cookies." if el else
                     "<strong>Visitor statistics</strong> through Google Analytics 4, <strong>only if you "
                     "accept</strong> them in the cookie settings.")
    if c["uses_contact_form"] or book:
        items_tail = ("<p>Τα υποχρεωτικά πεδία των φορμών είναι απαραίτητα για να σας απαντήσουμε· χωρίς αυτά "
                      "δεν μπορούμε να εξυπηρετήσουμε το αίτημά σας. Δεν ζητάμε και δεν χρειαζόμαστε άλλα "
                      "στοιχεία.</p>" if el else
                      "<p>The required form fields are needed to reply to you; without them we cannot handle "
                      "your request. We do not ask for, or need, anything else.</p>")
    else:
        items_tail = ("<p>Η ιστοσελίδα δεν διαθέτει φόρμες. Αν επικοινωνήσετε μαζί μας με email ή τηλέφωνο, "
                      "χρησιμοποιούμε τα στοιχεία σας μόνο για να σας απαντήσουμε.</p>" if el else
                      "<p>This website has no forms. If you contact us by email or phone, we only use your "
                      "details to reply to you.</p>")
    out.append(("data", "Ποια δεδομένα συλλέγουμε" if el else "What data we collect", ul(items) + items_tail))

    # 3. Purpose & legal basis -------------------------------------------
    head = (["Επεξεργασία", "Σκοπός", "Νομική βάση (ΓΚΠΔ)"] if el else
            ["Processing", "Purpose", "Legal basis (GDPR)"])
    via = ("φόρμα, email, τηλέφωνο" if el else "form, email, phone") if form else "email, " + ("τηλέφωνο" if el else "phone")
    rows = [["Μηνύματα (" + via + ")", "Απάντηση στο ερώτημά σας",
             "Άρθρο 6 παρ. 1 β' (ενέργειες πριν από σύμβαση) ή στ' (έννομο συμφέρον να απαντάμε σε "
             "όποιον μας γράφει)"] if el else
            ["Messages (" + via + ")", "Replying to your enquiry",
             "Art. 6(1)(b) (steps before a contract) or (f) (legitimate interest in replying to "
             "people who contact us)"]]
    if book:
        rows.append(["Κράτηση ραντεβού", "Προγραμματισμός και επιβεβαίωση του ραντεβού σας",
                     "Άρθρο 6 παρ. 1 β' (σύμβαση / ενέργειες πριν από σύμβαση)"] if el else
                    ["Appointment booking", "Scheduling and confirming your appointment",
                     "Art. 6(1)(b) (contract / steps before a contract)"])
    if news:
        rows.append(["Newsletter", "Αποστολή ενημερώσεων", "Άρθρο 6 παρ. 1 α' (συγκατάθεση)"] if el else
                    ["Newsletter", "Sending updates", "Art. 6(1)(a) (consent)"])
    if ga:
        rows.append(["Google Analytics 4", "Στατιστικά για τη βελτίωση της ιστοσελίδας",
                     "Άρθρο 6 παρ. 1 α' (συγκατάθεση)"] if el else
                    ["Google Analytics 4", "Statistics to improve the website", "Art. 6(1)(a) (consent)"])
    if maps:
        rows.append(["Χάρτης Google", "Εμφάνιση της τοποθεσίας μας, μόνο αν πατήσετε «Φόρτωση χάρτη»",
                     "Άρθρο 6 παρ. 1 α' (συγκατάθεση)"] if el else
                    ["Google map", "Showing our location, only if you click “Load map”",
                     "Art. 6(1)(a) (consent)"])
    rows.append(["Αρχεία καταγραφής διακομιστή", "Λειτουργία και ασφάλεια της ιστοσελίδας",
                 "Άρθρο 6 παρ. 1 στ' (έννομο συμφέρον)"] if el else
                ["Server logs", "Running and securing the website", "Art. 6(1)(f) (legitimate interest)"])
    rows.append(["Απαραίτητα cookies", "Αποθήκευση των επιλογών σας (cookies, γλώσσα)",
                 "Άρθρο 4 παρ. 5 ν. 3471/2006 (δεν απαιτείται συγκατάθεση)"] if el else
                ["Essential cookies", "Remembering your choices (cookies, language)",
                 "Art. 4(5) Greek Law 3471/2006 (no consent needed)"])
    tail = ("<p>Όπου η επεξεργασία βασίζεται στη συγκατάθεσή σας, μπορείτε να την ανακαλέσετε οποτεδήποτε, "
            "χωρίς να θίγεται η νομιμότητα της επεξεργασίας πριν από την ανάκληση. Δεν λαμβάνουμε "
            "αυτοματοποιημένες αποφάσεις ούτε κάνουμε κατάρτιση προφίλ.</p>" if el else
            "<p>Where processing is based on your consent, you can withdraw it at any time; this does not "
            "affect processing carried out before you withdrew it. We make no automated decisions and do "
            "no profiling.</p>")
    out.append(("purpose", "Σκοπός και νομική βάση" if el else "Purpose and legal basis",
                table(head, rows) + tail))

    # 4. Recipients ------------------------------------------------------
    rec = [
        "<strong>Data Master</strong> (Ελλάδα), ως εκτελών την επεξεργασία: ανάπτυξη και συντήρηση της "
        "ιστοσελίδας" + (" και του συστήματος κρατήσεων" if book else "") + "." if el else
        "<strong>Data Master</strong> (Greece), as processor: development and maintenance of the website"
        + (" and the booking system" if book else "") + ".",
        "<strong>HappyByte</strong> (Ελλάδα), ως εκτελών την επεξεργασία: φιλοξενία της ιστοσελίδας, "
        "email" + (" και αποστολή των μηνυμάτων της φόρμας" if form else "") + "." if el else
        "<strong>HappyByte</strong> (Greece), as processor: website hosting, email"
        + (" and delivery of form messages" if form else "") + ".",
    ]
    google = [x for x, on in ((("Χάρτες" if el else "Maps"), maps), ("Analytics", ga)) if on]
    if google:
        rec.append(f"<strong>Google Ireland Ltd</strong> ({', '.join(google)}), "
                   + ("μόνο εφόσον το αποδεχτείτε." if el else "only if you accept it."))
    rec_tail = ("<p>Οι εκτελούντες την επεξεργασία δεσμεύονται με σύμβαση (άρθρο 28 ΓΚΠΔ) να "
                "επεξεργάζονται τα δεδομένα μόνο για λογαριασμό μας. Δεν πωλούμε και δεν διαθέτουμε τα "
                "δεδομένα σας σε τρίτους για διαφημιστικούς σκοπούς. Μπορεί να τα γνωστοποιήσουμε σε δημόσιες "
                "αρχές μόνο όταν το επιβάλλει ο νόμος.</p>" if el else
                "<p>Processors are bound by contract (Article 28 GDPR) to process data only on our behalf. We "
                "do not sell your data or share it with third parties for advertising. We may disclose it to "
                "public authorities only where the law requires it.</p>")
    out.append(("recipients", "Αποδέκτες" if el else "Recipients", ul(rec) + rec_tail))

    # 5. Transfers -------------------------------------------------------
    if google:
        txt = ("<p>Η Google μπορεί να επεξεργαστεί δεδομένα και στις ΗΠΑ. Η Google LLC είναι πιστοποιημένη "
               "στο Πλαίσιο Προστασίας Δεδομένων ΕΕ–ΗΠΑ (EU–US Data Privacy Framework), για το οποίο η "
               "Ευρωπαϊκή Επιτροπή έχει εκδώσει απόφαση επάρκειας. Όλοι οι υπόλοιποι αποδέκτες "
               "επεξεργάζονται τα δεδομένα εντός της Ευρωπαϊκής Ένωσης.</p>" if el else
               "<p>Google may also process data in the United States. Google LLC is certified under the "
               "EU–US Data Privacy Framework, which is covered by a European Commission adequacy decision. "
               "All other recipients process data within the European Union.</p>")
    else:
        txt = ("<p>Τα δεδομένα σας δεν διαβιβάζονται εκτός της Ευρωπαϊκής Ένωσης.</p>" if el else
               "<p>Your data is not transferred outside the European Union.</p>")
    out.append(("transfers", "Διαβιβάσεις εκτός ΕΕ" if el else "Transfers outside the EU", txt))

    # 6. Retention -------------------------------------------------------
    head = ["Δεδομένα", "Διάρκεια διατήρησης"] if el else ["Data", "Retention"]
    rows = [["Μηνύματα" if el else "Messages", months(fm, lang)]]
    if book:
        rows.append(["Κρατήσεις ραντεβού (διαγράφονται αυτόματα)" if el else
                     "Appointment bookings (deleted automatically)", months(bm, lang)])
    if news:
        rows.append(["Newsletter", "Μέχρι να διαγραφείτε" if el else "Until you unsubscribe"])
    if ga:
        rows.append(["Google Analytics 4", months(am, lang)])
    rows.append(["Αρχεία καταγραφής διακομιστή" if el else "Server logs",
                 "Όσο τα τηρεί ο πάροχος φιλοξενίας για λόγους ασφαλείας" if el else
                 "As long as the hosting provider keeps them for security"])
    tail = ("<p>Αν προκύψει συνεργασία, τα στοιχεία σας τηρούνται για όσο απαιτεί ο νόμος (π.χ. φορολογική "
            "νομοθεσία).</p>" if el else
            "<p>If we go on to work together, your details are kept for as long as the law requires (e.g. tax "
            "law).</p>")
    out.append(("retention", "Πόσο διατηρούμε τα δεδομένα" if el else "How long we keep data",
                table(head, rows) + tail))

    # Sector clause ------------------------------------------------------
    sec = SECTOR.get(c.get("sector") or "")
    if sec:
        h, body = sec[lang]
        out.append(("sector", h, body))

    # 7. Rights ----------------------------------------------------------
    rights = (["<strong>Πρόσβαση</strong> στα δεδομένα σας", "<strong>Διόρθωση</strong> ανακριβών στοιχείων",
               "<strong>Διαγραφή</strong>", "<strong>Περιορισμό</strong> της επεξεργασίας",
               "<strong>Φορητότητα</strong> των δεδομένων", "<strong>Εναντίωση</strong> στην επεξεργασία που "
               "βασίζεται στο έννομο συμφέρον", "<strong>Ανάκληση της συγκατάθεσής σας</strong> οποτεδήποτε"]
              if el else
              ["<strong>Access</strong> your data", "<strong>Rectify</strong> inaccurate data",
               "<strong>Erasure</strong>", "<strong>Restrict</strong> processing",
               "<strong>Data portability</strong>", "<strong>Object</strong> to processing based on "
               "legitimate interest", "<strong>Withdraw your consent</strong> at any time"])
    pre = "<p>Έχετε δικαίωμα σε:</p>" if el else "<p>You have the right to:</p>"
    post = (f"<p>Για να ασκήσετε τα δικαιώματά σας, στείλτε μας email στο {mail}. Θα σας απαντήσουμε "
            f"δωρεάν, το αργότερο μέσα σε έναν μήνα. Μπορεί να σας ζητήσουμε να επιβεβαιώσετε την "
            f"ταυτότητά σας.</p>" if el else
            f"<p>To exercise your rights, email us at {mail}. We will reply free of charge within one month "
            f"at the latest. We may ask you to confirm your identity.</p>")
    out.append(("rights", "Τα δικαιώματά σας" if el else "Your rights", pre + ul(rights) + post))

    # 8. Complaint -------------------------------------------------------
    dpa = "<a href=\"https://www.dpa.gr\" target=\"_blank\" rel=\"noopener\">www.dpa.gr</a>"
    out.append(("complaint", "Δικαίωμα καταγγελίας" if el else "Right to complain",
                f"<p>Αν θεωρείτε ότι η επεξεργασία παραβιάζει τη νομοθεσία, μπορείτε να υποβάλετε καταγγελία "
                f"στην Αρχή Προστασίας Δεδομένων Προσωπικού Χαρακτήρα (ΑΠΔΠΧ), Λεωφ. Κηφισίας 1-3, "
                f"115 23 Αθήνα, {dpa}.</p>" if el else
                f"<p>If you believe the processing breaks the law, you can lodge a complaint with the Hellenic "
                f"Data Protection Authority (HDPA), 1-3 Kifisias Ave, 115 23 Athens, Greece, {dpa}.</p>"))

    # 9. Cookies ---------------------------------------------------------
    head = (["Όνομα", "Πάροχος", "Σκοπός", "Διάρκεια", "Κατηγορία"] if el else
            ["Name", "Provider", "Purpose", "Duration", "Category"])
    site = title
    rows = [[f"<code>{esc(c['consent_cookie'])}</code>", site,
             "Αποθηκεύει τις επιλογές σας για τα cookies" if el else "Stores your cookie choices",
             months(c["consent_cookie_months"], lang), "Απαραίτητα" if el else "Essential"]]
    if len(c["site_languages"]) > 1:
        rows.append(["<code>dm-lang</code> (local storage)", site,
                     "Θυμάται τη γλώσσα που επιλέξατε" if el else "Remembers the language you chose",
                     "Μέχρι να τη διαγράψετε" if el else "Until you clear it", "Απαραίτητα" if el else "Essential"])
    if ga:
        rows += [["<code>_ga</code>", "Google", "Διακρίνει μοναδικούς επισκέπτες" if el else
                  "Distinguishes unique visitors", "2 έτη" if el else "2 years", "Στατιστικά" if el else "Statistics"],
                 ["<code>_ga_&lt;ID&gt;</code>", "Google", "Διατηρεί την κατάσταση της επίσκεψης" if el else
                  "Keeps the state of the visit", "2 έτη" if el else "2 years", "Στατιστικά" if el else "Statistics"]]
    if maps:
        rows.append(["Cookies Google Maps (π.χ. <code>NID</code>)" if el else "Google Maps cookies (e.g. <code>NID</code>)",
                     "Google", "Λειτουργία του χάρτη, μόνο αφού πατήσετε «Φόρτωση χάρτη»" if el else
                     "Running the map, only after you click “Load map”", "Έως 6 μήνες" if el else "Up to 6 months",
                     "Εξωτερικό περιεχόμενο" if el else "External content"])
    pre = ("<p>Τα cookies είναι μικρά αρχεία που αποθηκεύονται στη συσκευή σας. Χρησιμοποιούμε μόνο όσα "
           "αναφέρονται παρακάτω. Τα <strong>απαραίτητα</strong> δεν χρειάζονται συγκατάθεση· όλα τα άλλα "
           "ενεργοποιούνται <strong>μόνο αν τα αποδεχτείτε</strong> και δεν φορτώνονται πριν από αυτό. "
           "Δεν χρησιμοποιούμε διαφημιστικά cookies.</p>" if el else
           "<p>Cookies are small files stored on your device. We only use the ones listed below. "
           "<strong>Essential</strong> cookies need no consent; all others are switched on <strong>only if "
           "you accept them</strong> and do not load before that. We use no advertising cookies.</p>")
    notes = []
    if ga:
        notes.append("Το Google Analytics 4 δεν καταγράφει ούτε αποθηκεύει διευθύνσεις IP. Έχουμε "
                     "απενεργοποιήσει τα Google signals και την εξατομίκευση διαφημίσεων." if el else
                     "Google Analytics 4 does not log or store IP addresses. We have turned off Google "
                     "signals and ads personalisation.")
    notes.append(("Μπορείτε να αλλάξετε ή να ανακαλέσετε τη συγκατάθεσή σας οποτεδήποτε από τον σύνδεσμο "
                  "«Ρυθμίσεις cookies» στο κάτω μέρος κάθε σελίδας ή από το κουμπί παρακάτω. Μπορείτε επίσης να "
                  "διαγράψετε τα cookies από τις ρυθμίσεις του φυλλομετρητή σας.") if el else
                 ("You can change or withdraw your consent at any time through the “Cookie settings” link at "
                  "the bottom of every page or the button below. You can also delete cookies in your browser "
                  "settings."))
    btn = (f"<p><button type=\"button\" class=\"btn\" data-cc=\"show-preferencesModal\" data-cookie-settings>"
           f"{UI[lang]['settings']}</button></p>")
    out.append(("cookies", "Cookies", pre + table(head, rows) + "".join(f"<p>{n}</p>" for n in notes) + btn))

    # 10. Changes --------------------------------------------------------
    out.append(("changes", "Αλλαγές σε αυτή την πολιτική" if el else "Changes to this policy",
                "<p>Μπορεί να ενημερώνουμε αυτή την πολιτική όταν αλλάζει η ιστοσελίδα ή η νομοθεσία. Η "
                "ημερομηνία της τελευταίας ενημέρωσης αναγράφεται στην αρχή της σελίδας.</p>" if el else
                "<p>We may update this policy when the website or the law changes. The date of the latest "
                "update is shown at the top of the page.</p>"))
    return out


def article(c, lang):
    secs = sections(c, lang)
    ui = UI[lang]
    toc = "".join(f"<li><a href=\"#{lang}-{sid}\">{h}</a></li>" for sid, h, _ in secs)
    body = "".join(f"<section id=\"{lang}-{sid}\"><h2><span class=\"n\">{i}.</span> {h}</h2>{b}</section>"
                   for i, (sid, h, b) in enumerate(secs, 1))
    return (f"<article data-l=\"{lang}\" lang=\"{lang}\"{' hidden' if lang != c['site_languages'][0] else ''}>"
            f"<h1>{ui['title']}</h1>"
            f"<p class=\"updated\">{ui['updated']}: <time datetime=\"{c['policy_last_updated']}\">"
            f"{fmt_date(c['policy_last_updated'], lang)}</time></p>"
            f"<nav class=\"toc\" aria-label=\"{ui['contents']}\"><h2>{ui['contents']}</h2><ol>{toc}</ol></nav>"
            f"{body}</article>")


def bi(c, key, wrap="span"):
    """Inline UI string in every site language; the script shows the active one."""
    first = c["site_languages"][0]
    return "".join(f"<{wrap} data-l=\"{l}\" lang=\"{l}\"{' hidden' if l != first else ''}>{UI[l][key]}</{wrap}>"
                   for l in c["site_languages"])


def page(c):
    t = c["theme"]
    langs = c["site_languages"]
    first = langs[0]
    brand = esc(tr(c["trading_title"], first))
    css = CSS
    for k, v in t.items():
        css = css.replace("{" + k + "}", v)
    switch = ""
    if len(langs) > 1:
        switch = ("<div class=\"lang\" role=\"group\" aria-label=\"Γλώσσα / Language\">" + "".join(
            f"<button type=\"button\" data-set-lang=\"{l}\" lang=\"{l}\" aria-pressed=\"{'true' if l == first else 'false'}\">"
            f"{'ΕΛ' if l == 'el' else l.upper()}</button>" for l in langs) + "</div>")
    ribbon = ""
    if c.get("demo"):
        ribbon = (f"<div class=\"dm-ribbon\">{bi(c, 'demo_rib')} <a href=\"../../\">{bi(c, 'demo_link')}</a></div>")
    titles = json.dumps({l: f"{UI[l]['title']} | {tr(c['trading_title'], l)}" for l in langs}, ensure_ascii=False)
    year = c["policy_last_updated"][:4]
    return f"""<!DOCTYPE html>
<html lang="{first}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Generated by legal/build.py from legal/sites.json. Do not edit by hand; rebuild instead. -->
    <title>{UI[first]['title']} | {brand}</title>
    <meta name="description" content="{UI[first]['title']}: {brand}">
    <meta name="theme-color" content="{t['dark']}">
    <style>{css}</style>
</head>
<body>
{ribbon}
<header class="top">
    <div class="wrap">
        <a class="brand" href="./">{brand}</a>
        <div class="top-r">
            <a class="back" href="./">&larr; {bi(c, 'back')}</a>
            {switch}
        </div>
    </div>
</header>

<main class="wrap doc">
{"".join(article(c, l) for l in langs)}
</main>

<footer>
    <div class="wrap">
        <span>&copy; {year} {brand}. {bi(c, 'rights')}</span>
        <span class="links"><a href="privacy.html">{bi(c, 'privacy')}</a> · <a href="#" data-cc="show-preferencesModal" data-cookie-settings>{bi(c, 'settings')}</a></span>
    </div>
</footer>

<script>
(function () {{
    var LANGS = {json.dumps(langs)}, TITLES = {titles};
    function store(v) {{ try {{ if (v === undefined) return localStorage.getItem("dm-lang"); localStorage.setItem("dm-lang", v); }} catch (e) {{ return null; }} }}
    function apply(lang) {{
        document.documentElement.lang = lang;
        document.title = TITLES[lang];
        document.querySelectorAll("[data-l]").forEach(function (el) {{ el.hidden = el.getAttribute("data-l") !== lang; }});
        document.querySelectorAll("[data-set-lang]").forEach(function (b) {{ b.setAttribute("aria-pressed", b.getAttribute("data-set-lang") === lang ? "true" : "false"); }});
    }}
    var lang = new URLSearchParams(location.search).get("lang");
    if (LANGS.indexOf(lang) < 0) lang = store();
    if (LANGS.indexOf(lang) < 0) lang = (navigator.language || "").toLowerCase().indexOf("en") === 0 && LANGS.indexOf("en") >= 0 ? "en" : LANGS[0];
    apply(lang);
    document.querySelectorAll("[data-set-lang]").forEach(function (b) {{
        b.addEventListener("click", function () {{
            var l = b.getAttribute("data-set-lang"); apply(l); store(l);
            try {{ var u = new URL(location.href); u.searchParams.set("lang", l); history.replaceState(null, "", u); }} catch (e) {{}}
        }});
    }});
    // privacy.html#cookies (linked from the site footer) lands on the cookie section of the active language.
    if (location.hash === "#cookies") {{
        var target = document.getElementById(lang + "-cookies");
        if (target) target.scrollIntoView();
    }}
    // "Cookie settings" reopens the consent banner (vanilla-cookieconsent handles data-cc itself).
    // Until a banner is installed, it jumps to the cookie section instead.
    document.querySelectorAll("[data-cookie-settings]").forEach(function (a) {{
        a.addEventListener("click", function (e) {{
            if (window.CookieConsent) return;
            e.preventDefault();
            var s = document.getElementById(document.documentElement.lang + "-cookies");
            if (s) s.scrollIntoView({{ behavior: "smooth" }});
        }});
    }});
}})();
</script>
</body>
</html>
"""


CSS = """
:root { --accent: {accent}; --accent-ink: {accent_ink}; --dark: {dark}; --on-dark: {on_dark}; --ink: {ink};
  --muted: {muted}; --bg: {bg}; --soft: {soft}; --line: {line}; --radius: {radius};
  --head: {head_font}; --body: {body_font}; }
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
body { margin: 0; font-family: var(--body); font-size: 16.5px; line-height: 1.7; color: var(--ink); background: var(--bg); -webkit-font-smoothing: antialiased; }
[hidden] { display: none !important; }
a { color: var(--accent-ink); }
:focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; }
.wrap { max-width: 880px; margin: 0 auto; padding: 0 20px; }
.dm-ribbon { padding: 7px 16px; background: #121110; color: #D2CBC2; font: 400 13px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; text-align: center; }
.dm-ribbon a { color: #fff; font-weight: 600; margin-left: 6px; }
.top { background: var(--dark); color: var(--on-dark); }
.top .wrap { display: flex; flex-wrap: wrap; gap: 10px 20px; align-items: center; justify-content: space-between; min-height: 68px; padding-top: 10px; padding-bottom: 10px; }
.brand { font-family: var(--head); font-weight: 700; font-size: 21px; color: #fff; text-decoration: none; }
.top-r { display: flex; align-items: center; gap: 18px; }
.back { color: var(--on-dark); text-decoration: none; font-size: 15px; }
.back:hover { color: #fff; }
.lang { display: inline-flex; border: 1px solid rgba(255,255,255,.35); border-radius: 999px; overflow: hidden; }
.lang button { font: 600 13px/1 var(--body); padding: 7px 11px; border: 0; background: transparent; color: var(--on-dark); cursor: pointer; }
.lang button[aria-pressed="true"] { background: #fff; color: var(--dark); }
.doc { padding-top: 48px; padding-bottom: 72px; }
h1, h2 { font-family: var(--head); line-height: 1.2; color: var(--ink); }
h1 { font-size: clamp(30px, 5vw, 42px); margin: 0 0 8px; }
h2 { font-size: 23px; margin: 0 0 12px; }
h2 .n { color: var(--accent); }
.updated { margin: 0 0 32px; color: var(--muted); font-size: 15px; }
.toc { background: var(--soft); border: 1px solid var(--line); border-radius: var(--radius); padding: 20px 24px; margin-bottom: 40px; }
.toc h2 { font-size: 15px; font-family: var(--body); text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin-bottom: 8px; }
.toc ol { margin: 0; padding-left: 22px; columns: 2 260px; column-gap: 32px; }
.toc li { break-inside: avoid; }
section { padding-top: 8px; margin-bottom: 36px; scroll-margin-top: 16px; }
section p, section ul { margin: 0 0 12px; }
section li { margin-bottom: 4px; }
.facts { display: grid; grid-template-columns: max-content 1fr; gap: 6px 20px; margin: 0 0 12px; padding: 18px 22px; background: var(--soft); border: 1px solid var(--line); border-radius: var(--radius); }
.facts dt { font-weight: 600; color: var(--muted); }
.facts dd { margin: 0; min-width: 0; overflow-wrap: anywhere; }
.tbl { overflow-x: auto; margin: 0 0 14px; border: 1px solid var(--line); border-radius: var(--radius); }
table { width: 100%; min-width: 560px; border-collapse: collapse; font-size: 15px; }
th, td { text-align: left; vertical-align: top; padding: 10px 14px; border-bottom: 1px solid var(--line); }
th { background: var(--soft); font-weight: 600; }
tr:last-child td { border-bottom: 0; }
code { font-size: 13.5px; background: var(--soft); border: 1px solid var(--line); border-radius: 4px; padding: 1px 5px; }
.btn { font: 600 15px/1 var(--body); padding: 12px 20px; border-radius: var(--radius); border: 0; background: var(--accent-ink); color: #fff; cursor: pointer; }
.btn:hover { filter: brightness(1.1); }
footer { background: var(--dark); color: var(--on-dark); font-size: 14.5px; padding: 28px 0; }
footer .wrap { display: flex; flex-wrap: wrap; gap: 10px 24px; justify-content: space-between; }
footer a { color: #fff; font-weight: 600; text-decoration: none; }
footer a:hover { text-decoration: underline; }
@media (max-width: 560px) {
  .facts { grid-template-columns: 1fr; gap: 0; }
  .facts dd { margin-bottom: 10px; }
  th, td { padding: 8px 10px; }
}
"""


def main(argv):
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    names = argv or list(cfg["sites"])
    for name in names:
        c = {**cfg["defaults"], **cfg["sites"][name]}
        out = ROOT / "websites" / name / "privacy.html"
        out.write_text(page(c), encoding="utf-8")
        print(f"built {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
