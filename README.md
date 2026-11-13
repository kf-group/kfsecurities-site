# kfsecurities.com

Static website for KF Securities Private Limited, built by `build.py` and published by GitHub Pages.

## Adding or removing services
Services come from **KF Ledger** (tables *Service Category* and *Service*, company `CO-KFS`).

1. Add, rename or deactivate the service in KF Ledger.
2. Run **publishAll** in the "KF websites publisher" Apps Script (or wait for the nightly run).
3. The script updates `data/catalog.json`; GitHub rebuilds the site in 1–2 minutes.

Each category gets its own page (`/services/<name>`), is listed in the sitemap and has structured data for Google.

## Website-only settings: `data/site.json`
- `categories`: public name and one-line description for a Ledger category.
- `order`: order of categories on the site.
- `hide_services`: Ledger service IDs that should not show on the website.
- `extra_categories`: services shown on the site that are not in KF Ledger yet (currently *Income tax & TDS*).

## Other settings
- `src/assets/config.js`: WhatsApp numbers, UPI ID, Razorpay Key ID (public key only), ARN.
- `src/content/*.html`: refund policy, terms, privacy policy, disclaimer.
