#!/usr/bin/env python3
"""Apply non-destructive FORME SPORT navigation + homepage teaser to index.html.
Run inside the FORME repository after copying sport.html and assets/forme-sport/.
"""
from pathlib import Path

index=Path('index.html')
if not index.is_file():
    raise SystemExit('ERROR: Run from the root of the forme-site repository, beside index.html.')
html=index.read_text(encoding='utf-8')
if 'href="sport.html"' in html:
    print('FORME SPORT links already present in index.html. No changes made.')
    raise SystemExit(0)
nav_old='<li><a href="#collection">Collection</a></li>'
if nav_old not in html:raise SystemExit('Could not find the existing header navigation. No changes made.')
html=html.replace(nav_old,nav_old+'\n        <li><a href="sport.html">Forme Sport</a></li>',1)
footer_old='<a href="#collection">Collection</a>'
if footer_old not in html:raise SystemExit('Could not find footer navigation. No changes made.')
# Last occurrence is in footer (first is inside header).
a=html.rfind(footer_old)
html=html[:a]+html[a:].replace(footer_old,footer_old+'\n        <a href="sport.html">Forme Sport</a>',1)

css='''
/* FORME SPORT teaser — follows the existing site tokens and grid. */
.forme-sport-teaser{display:grid;grid-template-columns:1fr 1fr;background:#19283f;color:var(--ivory);margin-top:0;min-height:440px}
.forme-sport-teaser__copy{align-self:center;padding:clamp(42px,7vw,100px);max-width:690px}
.forme-sport-teaser__copy .eyebrow{color:#d5d9e1}
.forme-sport-teaser__copy h2{font-family:var(--font-display);font-style:italic;font-weight:400;font-size:clamp(54px,6vw,88px);line-height:1.05;margin:15px 0 19px}
.forme-sport-teaser__copy p:not(.eyebrow){font-size:15px;line-height:1.8;max-width:42ch;margin-bottom:28px}
.forme-sport-teaser__copy a{display:inline-block;text-decoration:none;color:var(--ink);background:var(--ivory);padding:14px 22px;font-size:12px;font-weight:500}
.forme-sport-teaser__media{min-height:370px;overflow:hidden}
.forme-sport-teaser__media img{width:100%;height:100%;object-fit:cover;object-position:69% center}
@media(max-width:720px){.forme-sport-teaser{grid-template-columns:1fr}.forme-sport-teaser__copy{order:2;padding:42px var(--gutter) 48px}.forme-sport-teaser__media{order:1;min-height:310px;max-height:380px}}
'''
if '</style>' not in html:raise SystemExit('Could not find style end. No changes made.')
html=html.replace('</style>',css+'\n</style>',1)

section='''
  <!-- FORME SPORT — dedicated collection teaser -->
  <section class="forme-sport-teaser" id="forme-sport" aria-labelledby="forme-sport-teaser-title">
    <div class="forme-sport-teaser__copy">
      <p class="eyebrow">A new direction</p>
      <h2 id="forme-sport-teaser-title">Forme Sport.</h2>
      <p>Sport in its own form. Retro-inspired movement pieces, made for your everyday rotation.</p>
      <a href="sport.html">Explore FORME SPORT &rarr;</a>
    </div>
    <div class="forme-sport-teaser__media">
      <img src="assets/forme-sport/court-hero.webp" alt="FORME SPORT concept campaign on a street soccer court" loading="lazy" width="1600" height="790" decoding="async">
    </div>
  </section>

'''
anchor='  <!-- 5. Launch offer -->'
if anchor not in html:raise SystemExit('Could not find insertion point. No changes made.')
html=html.replace(anchor,section+anchor,1)
index.write_text(html,encoding='utf-8')
print('Updated index.html: header link, footer link and responsive FORME SPORT teaser.')
