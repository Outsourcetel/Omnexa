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
3. `street_address`: add the full street address; `cities` lists the cities served (each gets a landing page per service; add content in CITY_PAGES).
4. `form_endpoint`: optional JSON endpoint to store leads; otherwise the form opens WhatsApp prefilled.
5. Add real photos, verified client logos and testimonials (the old site's Pakistani client logos were NOT carried over).
6. Search Console: verify domain, submit /sitemap.xml. Create Google Business Profile.
7. 301-redirect plan: old site is a single URL, so no URL mapping is needed.

## Not included yet
Arabic pages (/ar/ with hreflang), blog, HVAC/electrical/plumbing/construction detail pages, photography.

## Design system
- Light base: white reads as hygiene (pest) and paper (ISO).
- Pest pages: green `#1c7c54` + hi-vis amber. ISO pages: blue `#1f4fbf` + seal gold. Set by `t-pest` / `t-iso` classes.
- Fonts: IBM Plex Sans (body), IBM Plex Sans Condensed (headings), IBM Plex Mono (standard numbers, labels). IBM Plex Sans Arabic is the planned match for /ar/.
- Illustrations and icons are inline SVG generated in `src/build.py` (`illus_pest`, `illus_iso`, `ICON`).
- Animations respect `prefers-reduced-motion` and the site works without JavaScript.

## Deploying on Vercel
`vercel.json` is in the repo root (static output from `public/`, no build step, trailing-slash URLs).
1. vercel.com > Add New > Project > import `Outsourcetel/Omnexa`.
2. Framework preset: Other. Leave Build Command and Install Command empty. Output Directory: `public`.
3. Deploy. Every push to `main` redeploys; other branches get their own preview URLs.
4. Domain: add `omnexasol.com` and `www.omnexasol.com` under Settings > Domains, make `www` redirect to the apex.
Note: Vercel's free Hobby plan is for non-commercial use; a company site needs Pro (verify current terms).
