# Data Master — Website Samples

Live samples of websites and website building blocks for small and mid-sized businesses, built by [Data Master](https://www.datamaster.gr):
ready-made templates, header styles and more to come. Browse them, pick what fits your business, and we adapt it to your brand, content and needs.

### 🔗 Live samples: **[datamaster-gr.github.io/templates](https://datamaster-gr.github.io/templates/)**

| Collection | What it is | Live |
|---|---|---|
| **Single-page websites** | 7 one-page website templates (below) | [Browse →](https://datamaster-gr.github.io/templates/websites/) |
| **Multi-page websites** | Complete sites with a page per service, team, fees and articles (below) | [Browse →](https://datamaster-gr.github.io/templates/multipage/) |
| **Header styles** | 10 live header styles: classic, centered, call to action, sticky, transparent, gradient, dark, icons, search, mega menu | [See them →](https://datamaster-gr.github.io/templates/components/headers/) |

---

## Single-page templates

| Template | Best for | Highlights | Live preview |
|---|---|---|---|
| **Modern Barber** | Barber shops, hair & beauty salons | Single-page, fully responsive, booking section, contact form | [View demo →](https://datamaster-gr.github.io/templates/websites/barber/) |
| **Minimalist Courier Services** | Couriers, logistics, delivery services | Clean minimalist layout, contact / quote request form | [View demo →](https://datamaster-gr.github.io/templates/websites/courier/) |
| **Sustainable Architecture & Development** | Architects, engineers, construction & design offices | Project showcase, Google Maps, contact form | [View demo →](https://datamaster-gr.github.io/templates/websites/architect/) |
| **Dental & Medical Practice** | Dentists, doctors, physiotherapists, clinics | Appointment request form, treatments & prices, FAQ, Greek & English | [View demo →](https://datamaster-gr.github.io/templates/websites/dental/) |
| **Accounting & Tax Office** | Accountants, tax advisors, business consultants | Monthly plans, "switch your accountant" section, meeting request form, Greek & English | [View demo →](https://datamaster-gr.github.io/templates/websites/accounting/) |
| **Law Firm** | Law firms, solo lawyers, notaries | Practice areas, team, fee approach, legal articles, consultation form, Greek & English; written within the Greek bar's advertising rules | [View demo →](https://datamaster-gr.github.io/templates/websites/law/) |
| **Hard Rock Band** | Bands, musicians, DJs, live acts | Dark stage look, tour dates on a taped setlist with ticket links, album & tracklist, video, booking form, newsletter; English | [View demo →](https://datamaster-gr.github.io/templates/websites/band/) |

## Multi-page templates

For businesses that need more than one page: a separate page for every service (each can rank on Google for its own searches), plus team, fees, articles and contact. Still plain static HTML: fast, secure, nothing to update.

| Template | Best for | Pages | Live preview |
|---|---|---|---|
| **Law Firm** | Law firms that want a page per practice area | 15 per language (Greek + English): home, practice areas + 6 area pages, team, fees, articles + 3 articles, contact. Greek URLs in Latin letters, hreflang, breadcrumbs, structured data (LegalService, FAQ, Article), `sitemap.xml` | [View demo →](https://datamaster-gr.github.io/templates/multipage/law/) |

**Editing a multi-page site:** don't edit the generated HTML. Each site has a `_src/` folder with the texts (`content_el.py`, `content_en.py`) and a build script that writes every page with the shared header, footer, menus and language switch:

```bash
python3 multipage/law/_src/build.py
```

Change the phone number or a practice area once, rebuild, and every page is updated. `_src/` is not published on GitHub Pages (Jekyll skips folders starting with `_`) and must not be uploaded to the client's server.

All business names, texts and images in the demos are sample content.

Every template comes with a **working contact form**: on the live site, messages go straight to the business owner's inbox (see [`contact-kit/`](contact-kit/README.md)). On these demo pages the forms only show their confirmation and send nothing.

Every template includes a bilingual **Privacy & Cookie Policy** page (`privacy.html`), generated from one shared text. See [`legal/`](legal/README.md).

## How it works

1. **Browse** the live demos and choose a template.
2. **Tell us about your business** — logo, colours, services, texts, photos.
3. **We customise and launch** your site on your own domain.

Interested? Get in touch at **[datamaster.gr](https://www.datamaster.gr)**.

## Repository structure

```
.
├── index.html            # Home: picks a collection (GitHub Pages landing page)
├── assets/               # Shared look (dm-site.css) and ΕΛ/EN switch (dm-site.js) for the showcase pages
├── components/
│   └── headers/          # 10 header styles, live
├── layouts/              # (future) wireframes and page layouts
├── DEPLOY.md             # Step-by-step guide for putting a site live on a client's domain
├── contact-kit/          # Contact form mailer (master copy) + per-client config sample
├── tools/                # sync-contact-kit.sh: copies the contact kit into every template
├── legal/                # Shared privacy-policy text + per-site variables → privacy.html
├── multipage/
│   ├── index.html        # Multi-page template gallery
│   └── law/              # Law Firm, multi-page (generated; sources in law/_src/)
└── websites/
    ├── index.html        # Single-page template gallery
    ├── barber/           # Modern Barber template
    ├── courier/          # Minimalist Courier Services template
    ├── architect/        # Sustainable Architecture template
    ├── dental/           # Dental & Medical Practice template
    ├── accounting/       # Accounting & Tax Office template
    ├── law/              # Law Firm template
    └── band/             # Hard Rock Band template
```

**Adding a new collection** (e.g. footers, forms, wireframes): put it in its own folder (`components/<name>/` or `layouts/<name>/`), reuse `assets/dm-site.css` and `assets/dm-site.js` (copy `components/headers/index.html` as a starting point), then add one entry to `COLLECTIONS` at the bottom of the root `index.html`. A group on the home page only shows once it has an entry.

Each template is a self-contained static site (HTML/CSS/JS) with its own `dm-contact/` folder, served directly by GitHub Pages from the default branch.

**Deploying a template for a client:** follow [`DEPLOY.md`](DEPLOY.md).

---

© 2026 [Data Master](https://www.datamaster.gr). All rights reserved.
