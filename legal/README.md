# Legal pages (`privacy.html`)

Every template ships with a «Πολιτική Απορρήτου & Cookies» page (compliance pack §1), generated from one shared text so a legal fix is made once and reaches every site.

| File | What it holds |
|---|---|
| `build.py` | The shared Greek + English policy text, the optional sector clauses and the page layout |
| `sites.json` | Per-client variables (pack §9) and each template's colours and fonts |
| `../websites/<site>/privacy.html` | Generated output. **Do not edit by hand** |

```bash
python3 legal/build.py           # rebuild all sites
python3 legal/build.py dental    # rebuild one site
```

## For a new client

1. Copy the template's entry in `sites.json` and fill in the business details (`business_name`, `trading_title`, `address`, `afm`, `gemi_number`, `email`, `phone`, `profession_regulator`).
2. Set the flags to what the site **actually** uses: `uses_contact_form`, `uses_booking`, `uses_ga4`, `uses_maps`, `uses_newsletter`, `site_languages`. Sections, table rows and cookies appear only for flags that are on.
3. Set `policy_last_updated` and, if agreed, the retention periods.
4. Rebuild, then check the cookie table against the live site.

`sector` is an optional extra: `health`, `law`, `accounting`, `engineer` or `courier` adds a short clause (health data, legal privilege, etc.). Leave it `null` for anything else.

## Assumptions the text makes

The page describes the setup the compliance pack requires, so these must be in place on the live site:

- hosting, email and the form handler on **HappyByte**; **Data Master** as processor under a DPA;
- a consent banner whose cookie is `consent_cookie` (default `cc_cookie`, vanilla-cookieconsent). The «Ρυθμίσεις cookies» links carry `data-cc="show-preferencesModal"`, so they reopen that banner once it is installed;
- Google Maps click-to-load, GA4 only after consent (Google signals and ads personalisation off), self-hosted fonts.

The demo values in `sites.json` are placeholders. The text is **not legal advice**: have it reviewed once by a lawyer (pack §11) before the first live site.
