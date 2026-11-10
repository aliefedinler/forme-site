# FORME — clothingforme.com

Group website for MKT 9780 (Digital Marketing, Baruch/Zicklin, Fall 2026). Started as the
week-3 *Initial website built* deliverable and updated weekly; current state as of **Nov 10, 2026**.

**FORME is a fictional brand.** Nothing on the site can be purchased. Semantic HTML, CSS and
vanilla JavaScript only — no frameworks, no build step, no backend. Deployed by Cloudflare Pages
from this repository's `main` branch.

## Change log (site updates by week)

| Date | Course week | Change |
|---|---|---|
| Sep 15–17 | Initial website | Homepage, four-piece collection, launch offer, brand story |
| Sep 23 | Content & traffic | GA4 behind a consent banner; event tracking |
| Sep 28 | SEO / content | Journal: four articles with Article structured data; sitemap, robots.txt |
| Sep 27–Oct 1 | AdSense or alternative | Ad slots, `ads.txt`, AdSense (pending) + Adsterra backup, house ads |
| Oct 8 | Social buttons & data | Share buttons with UTM-tagged URLs |
| Oct 11 | Your own banner | MyNext banner in the story section |
| Oct 22 | Affiliate links | Amazon Associates links (tag `formeessentia-20`) on the four products |
| Nov 10 | Content & traffic | FORME SPORT page, Brands section, Style Quiz, affiliate disclosure fixed site-wide, journal links switched to affiliate links, new pages tracked |

## 1. Files

```
index.html                  homepage (markup + CSS + JS in one file)
sport.html                  FORME SPORT concept collection
style-quiz.html             7-question style quiz
journal/                    index + four articles
sitemap.xml, robots.txt, ads.txt
ads/banner-*.html           Adsterra units, each isolated in its own iframe document
assets/
  forme.js                  consent gate + event tracking for every page except the homepage
  journal.css               shared styles for Journal, Sport and Quiz pages
  hero-debut-collection.jpg, product-*.jpg, og-cover.jpg, banner-mynext.jpg, social-*.png
  forme-sport/              FORME SPORT imagery (WebP) + og-sport.jpg share card
  brands/                   brand product photos (WebP), credited and linked on the page
tools/
  prepare_photos.py, make_assets.py, check.js
```

---

## 2. Preview

**Option A — open the file directly.** Double-click `index.html`. Everything works, with one
caveat: on `file://` some browsers block the async Clipboard API, so "Copy Offer Code" may fall
back to "select the code and press ⌘C / Ctrl+C". That fallback is intentional and is part of
what you're testing.

**Option B — local server (recommended, matches production).** From this folder:

```bash
python3 -m http.server 8000     # then open http://localhost:8000
```

**Debug mode.** Add `?debug=1` to the URL (e.g. `http://localhost:8000/?debug=1`) and open the
browser console. Tracked interactions print as `[FORME debug] <event_name> {...}`.
See §6 — this is a console log, not analytics.

---

## 3. Editing guide

### Product content
Each product is one `<li class="product">` in the `#collection` section. Two places hold the
same data and both must be updated together:

| Where | What it feeds |
|---|---|
| `data-id`, `data-name`, `data-price`, `data-colors`, `data-image`, `data-alt` on the `<li>` | the pop-up dialog and the analytics event |
| the visible `<h3>`, `.product__price`, `.product__colors`, `.product__desc`, `<img src>` and `<img alt>` | the card itself, and the page without JavaScript |

The dialog reads its description straight from `.product__desc`, so edit that paragraph once and
both views change. To add a fifth product, copy a whole `<li>` block — the grid reflows on its own.

### Colors, type and spacing
All tokens live in one `:root` block at the top of the `<style>`:

```css
--ivory:#F5F2EC   --ink:#191919    --stone:#8C8578
--line:#DBD5C9    --burgundy:#632D39
--maxw:1280px     --section-y / --s-1…--s-8 (spacing scale)
```

Change a value there and it propagates site-wide. Fonts are Instrument Serif (display) and
Inter (body) from Google Fonts, with Palatino/Georgia and system-sans fallbacks — if the font
request fails, the page still renders as designed.

### Copy
Headline, offer text and story sit directly in the markup. Keep the brand voice: concise,
confident, specific. Do not add sustainability, manufacturing, certification or durability
claims — none of them can be substantiated for a fictional brand, and unsupported claims are
exactly what the professor's grading looks for.

### Images
Point `JOBS` in `tools/prepare_photos.py` at new source files and re-run it — it crops to 4:5,
resizes, sharpens and compresses in one pass. See §4 for the attribution rules.

```bash
pip install pillow numpy
python3 tools/prepare_photos.py   # run from the project root
```

---

## 4. Imagery and attribution

The site uses photography supplied by the team on 15 Sep 2026, processed by
`tools/prepare_photos.py` (center-cover crop to the layout's 4:5 frames, resize, sharpen,
progressive JPEG). Originals were 1122×1402; nothing was retouched beyond that.

| File | Shows | Source | Photographer / rights holder | License |
|---|---|---|---|---|
| `hero-debut-collection.jpg` | full look — overshirt, tee, trouser | **TO FILL** | **TO FILL** | **TO FILL** |
| `product-essential-tee.jpg` | bone tee, flat | **TO FILL** | **TO FILL** | **TO FILL** |
| `product-everyday-hoodie.jpg` | heather grey hoodie, flat | **TO FILL** | **TO FILL** | **TO FILL** |
| `product-relaxed-trouser.jpg` | stone trouser, flat | **TO FILL** | **TO FILL** | **TO FILL** |
| `product-studio-overshirt.jpg` | olive overshirt, flat | **TO FILL** | **TO FILL** | **TO FILL** |
| `og-cover.jpg` | composite: wordmark + hero photo | derived from the hero image above | — | inherits the hero's license |
| `forme-sport/*.webp`, `og-sport.jpg` | FORME SPORT campaign image and five product mockups | concept imagery created by the team | FORME team | team-owned |
| `brands/eot-fatigue-pants-faded-green.webp` | Every Other Thursday Fatigue Pants | everyotherthursday.com product page | Every Other Thursday | brand's own image — credited and linked on the page |
| `brands/ds-twisted-merino-oat-marl.webp` | Daniel Simmons merino sweater | danielsimmons.co product page | Daniel Simmons | brand's own image — credited and linked on the page |

**Fill this table before the site is published or the report is submitted.** The professor
requires sourcing and attribution in standard academic format, and "images from the internet"
is not a source. For each image record the page URL, the photographer or rights holder, and the
license (e.g. Unsplash License, Pexels License, CC BY 4.0, or written permission). If a license
requires visible credit, add a credit line to the footer.

If any image turns out to be a retailer's own product photography, it cannot be used on a
published site without permission — replace it with a free-license or self-shot image, or keep
the illustrated flats that shipped in the previous version (regenerate them with
`python3 tools/make_assets.py`, which is still in the repo for exactly this reason).

### Honesty rules being observed
FORME is fictional, so the page states this in three places rather than implying a real store:
the note under the collection grid, the line at the bottom of each product dialog, and the
footer. If the images are ever replaced with photographs of actual FORME samples, those notes
should be updated — not deleted.

### Replacing an image later
1. Keep the same filename — no HTML changes needed.
2. Keep 4:5, or update the `width`/`height` attributes on the `<img>` so the browser still
   reserves the right space (this is what prevents layout shift).
3. Update both the `alt` attribute and the `data-alt` attribute on the product `<li>`.
4. Add the new source to the table above.
5. Re-run `python3 tools/prepare_photos.py` after pointing its `JOBS` list at the new files.

---

## 5. Optimization already in place

- One `<h1>`; `<h2>` per section; descriptive `<title>` and meta description.
- Open Graph + Twitter card metadata with a 1200×630 image.
- Explicit `width`/`height` on every image; `loading="lazy"` below the fold; hero is **not**
  lazy-loaded and carries `fetchpriority="high"`.
- All navigation, product names, prices, colors and descriptions work with JavaScript disabled.
- Keyboard: skip link, visible focus rings, Escape closes the menu and the dialog, focus returns
  to the button that opened the dialog, ~44px minimum touch targets.
- `prefers-reduced-motion` honored; animation limited to a 0.18–0.4 s hover/transition.
- No horizontal overflow at 375 / 768 / 1440 px, with or without JavaScript.
- Sticky header offset handled with `scroll-padding-top`, so anchors are never hidden behind it.

---

## 6. Measurement

GA4 (`G-DM67XJS2PV`) loads on every page **only after the visitor accepts** the consent banner.
The homepage has its own inline copy of the logic; every other page uses `assets/forme.js`. Any
element with `data-event` is tracked by one delegated click listener (`data-source`,
`data-product` and the outbound hostname are sent as parameters).

| Event | Where | Parameters |
|---|---|---|
| `collection_cta_click` | any "Explore Collection" CTA | `source` |
| `product_detail_view` | product dialog opens (homepage and Sport) | `product_id`, `source` |
| `offer_view` / `offer_code_copy` | launch offer seen / code copied | `code` |
| `outbound_product_click` | Amazon affiliate link (cards, dialog, journal, quiz) | `product_id`, `source`, `destination` |
| `outbound_brand_click` | Brands section photo or link | `product_id`, `source`, `destination` |
| `sport_cta_click` | links into FORME SPORT | `source` |
| `quiz_cta_click` | links into the quiz | `source` |
| `quiz_start` / `quiz_complete` | quiz started / finished | `quiz_style`, `matched_product` |
| `quiz_result_click`, `quiz_result_copy`, `quiz_retake` | actions on the result screen | `quiz_style`, `product_id` |
| `article_read_complete` | reader reaches the end of a journal article | `slug` |
| `ad_slot_view` / `ad_slot_click` / `ad_slot_fill` | ad inventory | `slot`, `network` |
| `consent_granted` | visitor accepts analytics | — |

KPIs for the performance report: sessions and users by source/medium (UTMs on share and quiz
links), collection CTR, product interest by `product_id`, quiz start → complete rate and style
mix, outbound affiliate CTR (compare with clicks in the Amazon Associates report), brand clicks,
article completion rate, consent rate. Visitors who decline cookies are not counted, so GA4
undercounts real traffic — state this in the report. **Do not report any figure the tools did not produce.**

### Evidence to save every week (for the Dec 3 presentation)

Screenshot and date-stamp: GA4 acquisition and engagement reports, Search Console performance,
each week's site change (before/after), any ad manager dashboard, and email/social metrics as we
add them. Keep them in one dated folder — the performance report is due at the presentation and
back-filling this is painful.

---

## 7. Deployment checklist (Cloudflare Pages)

Nothing here has been deployed. When the team is ready:

1. **Before uploading**, replace `https://forme.example.com/` with the real origin in the three
   absolute URLs in `<head>` (`canonical`, `og:url`, `og:image`). They are flagged with a comment.
   Relative paths elsewhere need no changes.
2. Push this folder to a Git repo, or drag it into Cloudflare Pages → *Direct Upload*.
3. Build settings: **framework preset `None`**, **build command empty**, **output directory `/`**
   (the repo root — `index.html` must sit at the top level).
4. Deploy, then open the live URL and confirm: images load, the mobile menu opens, a product
   dialog opens and closes, the offer code copies (HTTPS makes the Clipboard API available), and
   the console is clean.
5. Re-check the Open Graph card with a share-preview debugger; the image must be an absolute URL.
6. Add the analytics snippet (§6) and verify a live event before relying on the data.
7. Optional but cheap: `robots.txt` and a one-URL `sitemap.xml`, then submit the site to Google
   Search Console so SEO data starts accruing immediately — it takes days to populate, so do it
   the week the site goes up, not the week the report is due.
8. Confirm the footer still reads *Student project · Fictional brand · No purchases or payments.*

---

## 8. What was tested, and what wasn't

**Verified** in headless Chromium at 375×812, 768×1024 and 1440×900, from `file://`:

- no horizontal overflow at any of the three widths, with JavaScript on and off
- all six images load; no broken sources
- mobile menu opens, sets `aria-expanded`, closes on Escape and on link click
- product dialog opens with the right content, moves focus to the close button, closes on
  Escape, and returns focus to the button that opened it
- copy button reports success and fires `offer_code_copy` only on success; the manual-copy
  fallback path is implemented and exercised
- `offer_view` fires once, not repeatedly
- first Tab press reaches the skip link
- without JavaScript: nav links, product names, prices, colors and descriptions all remain visible
- anchor targets clear the sticky header at all three widths
- only console error is the Google Fonts request, which is blocked by this build sandbox's
  network policy — it will load normally on a real machine
- re-verified after the illustrated flats were replaced with photography (15 Sep 2026)

**Not yet tested** (do these before the check-in):

- real iOS Safari and Android Chrome on physical devices
- screen reader pass (VoiceOver / NVDA)
- clipboard behavior over HTTPS on the deployed site
- a Lighthouse run against the deployed URL
- automated contrast audit (contrast was designed to pass: ivory on burgundy ≈ 9.3:1, ink on
  ivory ≈ 15:1, but it hasn't been machine-verified)

---

## 9. Where this goes next

The syllabus wants each week's course topic layered onto the site. Hooks already in place:

| Week | Topic due | What to add |
|---|---|---|
| Sep 24 | Content & traffic | blog/journal entries, keyword-targeted copy, GA4 live |
| Oct 1 | AdSense or alternative | ad slot in a defined page region |
| Oct 8 | Social buttons & data | share buttons, Meta/TikTok pixel, UTM conventions |
| Oct 15 | Your own banner | self-promo banner, tracked as a new `data-event` CTA |
| Oct 22 | Affiliate links | affiliate section with disclosure |
| Nov 5 | Influencer strategy | creator landing page or discount-code variant |
| Nov 12 | Data analysis & optimization | A/B the hero headline or CTA; report the result |

Each addition should use the existing `data-event` pattern so the measurement story stays
consistent through the final report.
