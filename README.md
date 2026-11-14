# Omnexa Solutions website (static)

Pest control + ISO consultancy lead-generation site. 18 pages, no framework, no build dependencies beyond Python 3.

## Build
    python3 src/build.py        # writes ./public
    python3 -m http.server -d public 8000

Deploy `public/` to any static host (Cloudflare Pages, Netlify, S3+CDN, or the existing LiteSpeed server).
Serve `/404.html` as the error page and keep trailing-slash URLs. Redirect `www` -> apex with one 301.

## Edit
- `src/config.json`: phone, WhatsApp, email, address, city, GTM ID, form endpoint, and proof fields.
- `src/content.py`: all page copy (titles, descriptions, FAQs).
- `public/assets/`: CSS and JS.

## Before go-live checklist
1. `gtm_id`: add the GTM container ID; in GTM add GA4 + Google Ads conversion tags on events
   `generate_lead`, `click_whatsapp`, `click_to_call` (already pushed to dataLayer by site.js).
2. `proof`: add ISO certificate no./body, pest licence, CR, years in service ONLY when verified. Empty = not shown.
3. `street_address`: add the full street address; confirm primary city (Riyadh vs Jeddah) and set `primary_city`.
4. `form_endpoint`: optional JSON endpoint to store leads; otherwise the form opens WhatsApp prefilled.
5. Add real photos, verified client logos and testimonials (the old site's Pakistani client logos were NOT carried over).
6. Search Console: verify domain, submit /sitemap.xml. Create Google Business Profile.
7. 301-redirect plan: old site is a single URL, so no URL mapping is needed.

## Not included yet
Arabic pages (/ar/ with hreflang), blog, HVAC/electrical/plumbing/construction detail pages, photography.
