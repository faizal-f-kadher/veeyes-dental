# Veeyes Dental Hospital: website

A static site. It has no framework and no build step on the server. It uses one stylesheet, one small script and self-hosted fonts.

## Preview on your computer
Browsers block fonts on pages opened by double-clicking, so preview through a small local server instead:

    cd veeyes_redesign
    python -m http.server 8000

Then open http://localhost:8000. Stay online while you preview, because the photos and videos still load from the internet (see the next section).

## Before going live
1. **Run `python localize_media.py`.** It downloads every photo (currently on the Wix CDN) and every stock video and poster (Pexels and Mixkit) into `assets/media/`, then rewrites the pages to use those local copies. The Wix links stop working once the Wix site is closed.
2. **Upload the folder** to any static host. Hosting setup is already included:
   - `.htaccess` for Apache/cPanel: clean URLs (/about instead of /about.html), 301 redirects from the old Wix addresses, the 404 page and caching.
   - `_redirects` for Netlify.
   - `vercel.json` for Vercel.
3. **Search engines:** `sitemap.xml` and `robots.txt` are ready to use. Page addresses match the old site, so existing Google rankings carry over.

## Pages (mapped from the old site)
| Page | File |
|---|---|
| Home | index.html |
| About, both chief surgeons, the full team | about.html |
| Treatments overview (5 groups) | treatments.html |
| 19 treatment pages | teeth-alignment.html, invisalign.html, … (same slugs as before) |
| Smile Gallery: 21 before/after sliders plus 2 photos, filterable | smile-gallery.html |
| Hospital: OT, surgical ICU, NOIS, sterilisation, 17 photos | clinic-gallery.html |
| Blog and 4 articles | blog.html, post/*.html |
| Contact, with Google Maps for both hospitals | contact.html |
| Book appointment | appointment.html |

## How booking works
There is no server, so the booking form opens WhatsApp with the patient's details already filled in, sent to the hospital they choose:
- Coimbatore: +91 88256 18228
- Tiruppur: +91 93447 28252

Links from treatment pages fill in the treatment automatically (for example, appointment.html?t=teeth-alignment). Adding `&c=tiruppur` selects the Tiruppur hospital. On phones, a bottom bar offers Call (choose the hospital), WhatsApp and Book.

## Editing content
All text lives in `_source/content.py`; the icon set is in `_source/icons.py` (each icon is a small SVG drawing, easy to recolour or swap). Edit it, then run `python build.py` from the `_source` folder to regenerate the pages. The build expects the `static/` and `extra/` folders next to it, as in the original project.

## Stock video (free for commercial use, no attribution needed)
- Hero: Pexels 7803018 (young girl smiling in the dental chair)
- Treatments section and treatment pages: Pexels 5356196, 4490544
- Digital dentistry: Pexels 5356055 (dentist explaining an X-ray)
- Kids: Pexels 7803498
- Teeth alignment: Mixkit 24630 (woman with braces)
- Teeth whitening and cosmetic dentistry: Mixkit 39580

All other photos are the clinic's own.

## Please confirm with the clinic
- **Phone numbers.** The old blog posts list 0422 438 3000, and the old site's code contains +91 77080 04372. The new site uses only 0422 253 3333 / 88256 18228 (Coimbatore) and 0421 433 3366 / 93447 28252 (Tiruppur).
- **Opening hours.** None appear on the old site, so none are shown.
- **Doctor photos.** Replace these when the new ones arrive. They're set in `TEAM` and `LEADS` in content.py. Use square photos for the team and 4:5 portraits for the two chief surgeons.
- **Reviews.** Only the old site's 3 testimonials are used. Add a link to the Google Business profile if there is one.
- **Pages dropped:** the Wix template demos (Online Coaching, Corporate Life and the other "service-page" and "booking-calendar" pages), the empty Events page, and "Inflation Facility" (its text was about cost control, not a facility). All of these redirect.
