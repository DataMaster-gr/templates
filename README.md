# Data Master — Website Templates

Ready-made, responsive website templates for small and mid-sized businesses, built by [Data Master](https://www.datamaster.gr).
Browse the live demos, pick the one closest to your business, and we adapt it to your brand, content and needs.

### 🔗 Live demo: **[datamaster-gr.github.io/templates](https://datamaster-gr.github.io/templates/)**

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
├── index.html            # Template index (GitHub Pages landing page)
├── DEPLOY.md             # Step-by-step guide for putting a site live on a client's domain
├── contact-kit/          # Contact form mailer (master copy) + per-client config sample
├── tools/                # sync-contact-kit.sh: copies the contact kit into every template
├── legal/                # Shared privacy-policy text + per-site variables → privacy.html
└── websites/
    ├── barber/           # Modern Barber template
    ├── courier/          # Minimalist Courier Services template
    ├── architect/        # Sustainable Architecture template
    ├── dental/           # Dental & Medical Practice template
    ├── accounting/       # Accounting & Tax Office template
    └── law/              # Law Firm template
```

Each template is a self-contained static site (HTML/CSS/JS) with its own `dm-contact/` folder, served directly by GitHub Pages from the default branch.

**Deploying a template for a client:** follow [`DEPLOY.md`](DEPLOY.md).

---

© 2026 [Data Master](https://www.datamaster.gr). All rights reserved.
