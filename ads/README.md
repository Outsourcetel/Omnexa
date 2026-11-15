# Google Ads plan: Omnexa Solutions (Saudi Arabia)

Files in this folder (regenerate with `python3 ads/build_ads.py`):

| File | What it is |
|---|---|
| `keyword-plan.csv` | 229 keywords x 2 match types, by campaign and ad group, with the landing page and launch phase |
| `ad-copy.csv` | One responsive search ad per ad group: 15 headlines max (30 characters), 4 descriptions (90 characters), all lengths checked |
| `negative-keywords.csv` | Negative keywords by campaign group |

**Not included: keyword volumes, bids and budgets.** I have no access to Google Keyword Planner or an Ads account, so I did not invent numbers.
Validate every keyword in Keyword Planner (language Arabic or English, location Riyadh and Jeddah) before launch and drop or merge anything with no volume.

## 1. Goals and how success is counted
- **Pest control:** enquiries (WhatsApp click, phone click, form submit) from Riyadh and Jeddah.
- **ISO consultancy:** consultation enquiries from companies in Riyadh and Jeddah.
- **ISO training:** quote requests. Training ads and pages never state prices.

## 2. Account structure
6 campaigns, 50 ad groups. Language is set per campaign, so Arabic and English never compete for the same budget.

| Campaign | Language | Ad groups |
|---|---|---|
| 01 Pest, Arabic | Arabic | General (Riyadh), General (Jeddah), Termite, Rodents, Cockroaches, Bed bugs, Fumigation, Mosquito and dengue, Birds, Snakes and wildlife, Commercial |
| 02 Pest, English | English | same 11 |
| 03 ISO Consultancy, Arabic | Arabic | General (Riyadh), General (Jeddah), ISO 9001, ISO 22000 and HACCP, ISO 45001, ISO 14001, ISO 27001, Other standards |
| 04 ISO Consultancy, English | English | same 8 |
| 05 ISO Training, Arabic | Arabic | General, ISO 9001, ISO 14001, ISO 45001, ISO 22000 and HACCP, ISO 27001 |
| 06 ISO Training, English | English | same 6 |

- **Why split by service:** the three services have different buyers, different budgets and different conversion value.
- **Why Arabic and English are separate:** Arabic search is large in Saudi Arabia, and the Arabic landing pages are different pages.
- **Ad group to page:** every ad group points at the most specific page (for example, termite keywords go to `/ar/pest-control/termite-control/`). All 50 landing pages exist on the site.

## 3. Targeting and settings
- **Locations:** Riyadh and Jeddah (city targeting). Choose "Presence" (people in or regularly in the location), not "Presence or interest".
- **Languages:** Arabic campaigns target Arabic; English campaigns target English.
- **Networks:** Search only at first. Turn off the Search Partners and Display expansion.
- **Match types:** phrase and exact only at launch. Do not use broad match until there are conversions to guide it.
- **Schedule:** the Saudi work week is Sunday to Thursday. Pest control and emergency-type searches can run every day. ISO consultancy and training enquiries can be limited to Sunday to Thursday daytime plus Saturday evening for WhatsApp, if nobody answers on Fridays. Check the time zone is UTC+3.
- **Ad rotation and assets:** add sitelinks (Termite, Rodents, Commercial, How it works), callouts ("Free site inspection", "Written service reports", "WhatsApp enquiries"), a call asset (`+966 50 039 3660`) and a location asset (Riyadh and Jeddah offices).
- **Bidding:** start with Maximize clicks with a maximum CPC limit (no more than you can afford per click), then move to Maximize conversions after about 30 conversions per campaign. Do not start on target CPA with no data.

## 4. Launch in phases
- **Phase 1** (129 keywords, the highest-intent searches): Pest General (Riyadh, Jeddah), Termite, Rodents, Cockroaches, Commercial; ISO General (Riyadh, Jeddah), ISO 9001, ISO 22000 and HACCP; Training ISO 9001 and HACCP.
- **Phase 2** (73 keywords, after the first 2 to 3 weeks): bed bugs, fumigation, mosquito, ISO 45001, 14001, 27001, other training.
- **Phase 3** (27 keywords): birds, snakes and wildlife, other standards. These are smaller searches and need page and photo improvements first.

## 5. Conversion tracking (set up before any spend)
1. Add the Google Tag Manager ID in `src/config.json` (`gtm_id`) and rebuild. Nothing is tracked until this is done.
2. The site already sends three events: `generate_lead` (form), `click_whatsapp` and `click_to_call`.
3. In GTM, create a GA4 event tag for each, then import the three as conversions in Google Ads (or use the Ads conversion tag directly).
4. Count `generate_lead` and `click_whatsapp` as primary conversions. Count `click_to_call` too, and consider a Google forwarding number for call reporting.
5. The WhatsApp message carries the page address, so you can see in WhatsApp which page the enquiry came from.
6. Add a cookie or consent notice if your legal advice requires one for tracking.

## 6. Ad copy rules that keep the ads approved
- No prices, discounts or "cheap". No "best", "number one" or "guaranteed". Ads follow the same no-pricing rule as the site.
- Claims used in the ads are ones the pages support: free site inspection, written service report, free ISO consultation, we prepare you for the audit, request a quote.
- **Do not add** a licence, accreditation or "certified" claim to any ad until it is shown on the site with the number. Google and Saudi regulators may ask for proof.
- ISO ads must say "consultancy" and "we prepare you for the audit". They must not imply that Omnexa issues the certificate.
- Do not use competitor names, including certification bodies, as keywords or in ad text.

## 7. Negative keywords
See `negative-keywords.csv`. Key points:
- Job seekers, free downloads and DIY searches are blocked everywhere.
- Pest campaigns block ISO and training terms. ISO consultancy campaigns block "training" and "course" terms, so those searches go to the training campaigns. Training campaigns block pest and template searches.
- Review the Search Terms report every week for the first month and add new negatives.

## 8. Weekly routine for the first month
1. Search Terms report: add negatives, add new exact keywords for terms that convert.
2. Compare campaigns by cost per enquiry. Pause ad groups with spend and no enquiries after about 2 weeks.
3. Check ad strength and the asset report: replace headlines with low performance.
4. Check the landing pages in Search Console (indexing, mobile usability) and PageSpeed on a phone.

## 9. What I need from you
- A Google Ads account (or access), the Tag Manager ID and the daily budget per campaign.
- Confirmation of the working hours and who answers WhatsApp and calls, and in which languages.
- The licence and certificate numbers you want shown (see the site checklist), so they can support the ads.
- A decision on how much Arabic versus English budget to start with.
