# FORME — Initial Website

Single-page storefront prototype for MKT 9780 (Digital Marketing, Baruch/Zicklin, Fall 2026),
week 3 deliverable: *Initial website built*.

**FORME is a fictional brand.** Nothing on the page can be purchased, and the photography is
stand-in imagery, not pictures of FORME products. Semantic HTML, CSS and vanilla JavaScript
only — no frameworks, no build step, no API keys, no backend.

---

## 1. Files

```
index.html                 the entire site (markup + CSS + JS in one file)
README.md                  this file
assets/
  hero-debut-collection.jpg    1100×1375  hero image
  product-essential-tee.jpg     800×1000  4:5 product image
  product-everyday-hoodie.jpg   800×1000
  product-relaxed-trouser.jpg   800×1000
  product-studio-overshirt.jpg  800×1000
  og-cover.jpg                 1200×630   Open Graph / social share card
  favicon.svg
tools/
  prepare_photos.py         crops/compresses supplied photography into /assets
  make_assets.py            regenerates illustrated flats, if photography is ever pulled
  check.js                  automated layout/interaction checks (Node + Playwright)
```

Total page weight: **~560 KB** including all images. All asset paths are relative, so the
site works from a local file, a subfolder, or a domain root without edits.

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

## 6. Measurement foundation

Four events are instrumented through one helper, `window.FORME.track(name, payload)`:

| Event | Fires when | Payload |
|---|---|---|
| `collection_cta_click` | any "Explore Collection" CTA is clicked | `source`: `announcement` / `header` / `hero_primary` |
| `product_detail_view` | a product dialog opens | `product_id`, `product_name` |
| `offer_view` | the offer section is ≥40% visible — **once per page view** | `code` |
| `offer_code_copy` | **only after the copy actually succeeds** | `code`, `method` |

CTAs carry `data-event` and `data-source` attributes and are captured by a single delegated
click listener, so adding a new tracked CTA means adding the attributes — no new JavaScript.

**These are console logs, not analytics.** Nothing is sent anywhere, nothing is stored, and no
visitor data is collected. Events are held in `window.FORME.events` for the current page view and
printed only when `?debug=1` is present. Any number we report to the class must come from a real
analytics tool, not from this array.

### Connecting real analytics later

In `index.html`, find the `send()` function inside the `window.FORME` block. The hook is marked:

```js
/* Connect a real tool here, e.g.:
   if (window.gtag) gtag('event', name, payload);
   if (window.plausible) plausible(name, { props: payload });          */
```

Uncomment one line and add that tool's snippet in `<head>`. Recommended for this course:
**Google Analytics 4** (free, gives the acquisition/engagement reports the final performance
report asks for) plus **Google Search Console** (impressions, clicks, average position, queries —
the SEO evidence for the Sep 17 week). Cloudflare Web Analytics is a cookie-free alternative that
needs no consent banner.

Once connected, these four custom events become the KPIs we can actually report:

| Metric | Formula | What it tells us |
|---|---|---|
| Collection click-through rate | `collection_cta_click` ÷ sessions | does the hero message earn a click |
| Product interest | `product_detail_view` per session, by `product_id` | which of the four pieces pulls attention |
| Offer engagement | `offer_view` ÷ sessions | how many visitors reach the offer at all |
| Code-copy rate | `offer_code_copy` ÷ `offer_view` | conversion intent on the offer itself |
| Source mix | `source` on `collection_cta_click` | which CTA placement earns the click |

Traffic, cost and revenue for the final report come from GA4 plus the ad platforms we add in
later weeks. **Do not report any figure the tools did not produce.**

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
