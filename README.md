# Data Master — Website Samples

Live samples of websites and website building blocks for small and mid-sized businesses, built by [Data Master](https://www.datamaster.gr):
ready-made templates, header styles and more to come. Browse them, pick what fits your business, and we adapt it to your brand, content and needs.

### 🔗 Live samples: **[datamaster-gr.github.io/templates](https://datamaster-gr.github.io/templates/)**

| Collection | What it is | Live |
|---|---|---|
| **Ready-made websites** | 6 complete website templates (below) | [Browse →](https://datamaster-gr.github.io/templates/websites/) |
| **Header styles** | 10 live header styles: classic, centered, call to action, sticky, transparent, gradient, dark, icons, search, mega menu | [See them →](https://datamaster-gr.github.io/templates/components/headers/) |

---

## Templates

| Template | Best for | Highlights | Live preview |
|---|---|---|---|
| **Modern Barber** | Barber shops, hair & beauty salons | Single-page, fully responsive, booking section, contact form | [View demo →](https://datamaster-gr.github.io/templates/websites/barber/) |
| **Minimalist Courier Services** | Couriers, logistics, delivery services | Clean minimalist layout, contact / quote request form | [View demo →](https://datamaster-gr.github.io/templates/websites/courier/) |
| **Sustainable Architecture & Development** | Architects, engineers, construction & design offices | Project showcase, Google Maps, contact form | [View demo →](https://datamaster-gr.github.io/templates/websites/architect/) |
| **Dental & Medical Practice** | Dentists, doctors, physiotherapists, clinics | Appointment request form, treatments & prices, FAQ, Greek & English | [View demo →](https://datamaster-gr.github.io/templates/websites/dental/) |
| **Accounting & Tax Office** | Accountants, tax advisors, business consultants | Monthly plans, "switch your accountant" section, meeting request form, Greek & English | [View demo →](https://datamaster-gr.github.io/templates/websites/accounting/) |
| **Law Firm** | Law firms, solo lawyers, notaries | Practice areas, team, fee approach, legal articles, consultation form, Greek & English; written within the Greek bar's advertising rules | [View demo →](https://datamaster-gr.github.io/templates/websites/law/) |

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
└── websites/
    ├── index.html        # Template gallery
    ├── barber/           # Modern Barber template
    ├── courier/          # Minimalist Courier Services template
    ├── architect/        # Sustainable Architecture template
    ├── dental/           # Dental & Medical Practice template
    ├── accounting/       # Accounting & Tax Office template
    └── law/              # Law Firm template
```

**Adding a new collection** (e.g. footers, forms, wireframes): put it in its own folder (`components/<name>/` or `layouts/<name>/`), reuse `assets/dm-site.css` and `assets/dm-site.js` (copy `components/headers/index.html` as a starting point), then add one entry to `COLLECTIONS` at the bottom of the root `index.html`. A group on the home page only shows once it has an entry.

Each template is a self-contained static site (HTML/CSS/JS) with its own `dm-contact/` folder, served directly by GitHub Pages from the default branch.

**Deploying a template for a client:** follow [`DEPLOY.md`](DEPLOY.md).

---

© 2026 [Data Master](https://www.datamaster.gr). All rights reserved.
