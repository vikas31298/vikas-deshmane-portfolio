"""Generate products/<slug>.html pages and the Products section in index.html from products.json.

Run:  python build_products.py
Edit products.json, re-run, done.
"""
import json, html, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
products = json.load(open(os.path.join(ROOT, 'products.json'), encoding='utf8'))
os.makedirs(os.path.join(ROOT, 'products'), exist_ok=True)

e = html.escape

import build_covers
import build_tabs
build_covers.build()

def cover(p):
    return p.get('image') or f"assets/products/{p['slug']}.svg"

def head(title, desc, depth=1):
    rel = '../' * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(title)} · Vikas Deshmane</title>
  <meta name="description" content="{e(desc)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{rel}styles.css?v=4">
</head>
<body>
  <header class="nav" id="top">
    <div class="container nav__inner">
      <a href="{rel}index.html" class="nav__brand">Vikas Deshmane<span>.</span></a>
      <nav class="nav__links" id="navLinks">
        <a href="{rel}index.html#about">About</a>
        <a href="{rel}index.html#products" class="active">Products</a>
        <a href="{rel}index.html#experience">Experience</a>
        <a href="{rel}index.html#skills">Skills</a>
        <a href="{rel}index.html#contact">Contact</a>
      </nav>
      <div class="nav__actions">
        <a href="{rel}assets/Vikas_Deshmane_CV.docx" class="btn btn--ghost btn--sm" download>Download CV</a>
        <button class="nav__toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button>
      </div>
    </div>
  </header>
"""

def foot(depth=1):
    rel = '../' * depth
    return f"""
  <footer class="footer">
    <div class="container footer__inner">
      <span>© <span id="year"></span> Vikas Deshmane</span>
      <a href="{rel}index.html#products">All products</a>
    </div>
  </footer>
  <script src="{rel}script.js?v=4"></script>
</body>
</html>
"""

def product_page(p, prev_p, next_p):
    metrics = ''.join(f'<div class="stat"><span class="stat__num">{e(m["value"])}</span><span class="stat__label">{e(m["label"])}</span></div>' for m in p['hero_metrics'])
    strategy = ''.join(f'<li>{e(s)}</li>' for s in p['strategy'])
    arch = ''.join(
        f'<div class="arch__layer"><div class="arch__name">{e(l["layer"])}</div><div class="arch__items">' +
        ''.join(f'<span>{e(i)}</span>' for i in l['items']) + '</div></div>'
        for l in p['architecture'])
    impact = ''.join(f'<div class="impact"><span class="impact__value">{e(i["value"])}</span><p>{e(i["detail"])}</p></div>' for i in p['impact'])
    decisions = ''.join(f'<li>{e(d)}</li>' for d in p['decisions'])
    stack = ''.join(f'<li>{e(s)}</li>' for s in p['stack'])
    prev_link = f'<a href="{prev_p["slug"]}.html" class="pager__link"><small>Previous</small>{e(prev_p["name"])}</a>' if prev_p else '<span></span>'
    next_link = f'<a href="{next_p["slug"]}.html" class="pager__link pager__link--next"><small>Next</small>{e(next_p["name"])}</a>' if next_p else '<span></span>'

    tab_nav, tab_panels = build_tabs.tabs_for(p['slug'])
    return head(p['name'], p['tagline']) + f"""
  <section class="phero">
    <div class="container">
      <a href="../index.html#products" class="back">← All products</a>
      <p class="eyebrow">{e(p['category'])}</p>
      <h1 class="phero__title">{e(p['name'])}</h1>
      <p class="phero__tagline">{e(p['tagline'])}</p>
      <dl class="phero__facts">
        <div><dt>Organisation</dt><dd>{e(p['org'])}</dd></div>
        <div><dt>Role</dt><dd>{e(p['role'])}</dd></div>
        <div><dt>Period</dt><dd>{e(p['period'])}</dd></div>
      </dl>
      <figure class="phero__cover"><img src="../{cover(p)}" alt="{e(p['name'])} illustration"></figure>
    </div>
  </section>

  {tab_nav}<div class="tabpanel" id="tab-overview" role="tabpanel">
  <section class="section section--tight">
    <div class="container">
      <div class="hero__card reveal"><div class="stat-grid stat-grid--4">{metrics}</div></div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container detail">
      <div class="detail__side reveal"><p class="eyebrow">Business context</p><h2>The problem</h2></div>
      <div class="detail__main reveal"><p class="lead-text">{e(p['context'])}</p></div>
    </div>
  </section>

  <section class="section section--tight section--alt">
    <div class="container detail">
      <div class="detail__side reveal"><p class="eyebrow">My role</p><h2>Scope and ownership</h2></div>
      <div class="detail__main reveal"><p class="lead-text">{e(p['role_scope'])}</p></div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container detail">
      <div class="detail__side reveal"><p class="eyebrow">Product strategy</p><h2>How I approached it</h2></div>
      <div class="detail__main reveal"><ol class="numbered">{strategy}</ol></div>
    </div>
  </section>

  <section class="section section--tight section--alt">
    <div class="container">
      <div class="section__head reveal"><p class="eyebrow">Tech architecture</p><h2>How the platform is put together</h2><p class="section__sub">{e(p['architecture_summary'])}</p></div>
      <div class="arch reveal">{arch}</div>
      <div class="arch__stack reveal"><span>Key technologies</span><ul class="chips">{stack}</ul></div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container">
      <div class="section__head reveal"><p class="eyebrow">Business impact</p><h2>What moved</h2></div>
      <div class="impacts">{impact}</div>
    </div>
  </section>

  <section class="section section--tight section--alt">
    <div class="container detail">
      <div class="detail__side reveal"><p class="eyebrow">Key decisions</p><h2>Trade-offs I would defend</h2></div>
      <div class="detail__main reveal"><ul class="bullets">{decisions}</ul></div>
    </div>
  </section>

  </div>
  {tab_panels}
  <section class="section section--tight">
    <div class="container pager">{prev_link}{next_link}</div>
  </section>

  <section class="section section--contact">
    <div class="container contact reveal">
      <h2>Want to go deeper on this product?</h2>
      <p class="contact__lead">Happy to walk through the architecture, the numbers and the decisions in a conversation.</p>
      <div class="contact__links">
        <a class="btn btn--primary" href="mailto:vikasdeshmane.iiml@gmail.com">Email me</a>
        <a class="btn btn--ghost" href="https://www.linkedin.com/in/vikasdeshmane" target="_blank" rel="noopener">LinkedIn</a>
      </div>
    </div>
  </section>
""" + foot()

# --- write product pages
for i, p in enumerate(products):
    prev_p = products[i - 1] if i > 0 else None
    next_p = products[i + 1] if i < len(products) - 1 else None
    with open(os.path.join(ROOT, 'products', p['slug'] + '.html'), 'w', encoding='utf8') as f:
        f.write(product_page(p, prev_p, next_p))

# --- home page section
cards = ''
for p in products:
    ms = ''.join(f'<li><strong>{e(m["value"])}</strong> {e(m["label"])}</li>' for m in p['hero_metrics'][:3])
    cards += f"""
        <a class="pcard reveal" href="products/{p['slug']}.html">
          <div class="pcard__media"><img src="{cover(p)}" alt="{e(p['name'])} illustration" loading="lazy"></div>
          <div class="case__head"><span class="case__tag">{e(p['category'])}</span><span class="case__org">{e(p['org'])} · {e(p['period'])}</span></div>
          <h3>{e(p['name'])}</h3>
          <p>{e(p['tagline'])}</p>
          <ul class="case__results">{ms}</ul>
          <span class="pcard__cta">View product details →</span>
        </a>"""

section = f"""<!-- PRODUCTS:START -->
  <section class="section section--alt" id="products">
    <div class="container">
      <div class="section__head reveal">
        <p class="eyebrow">Products</p>
        <h2>The products I have led.</h2>
        <p class="section__sub">Each product has its own page covering the business context, my role, product strategy, technical architecture, business impact and the key decisions behind it.</p>
      </div>
      <div class="pcards">{cards}
      </div>
    </div>
  </section>
  <!-- PRODUCTS:END -->"""

idx_path = os.path.join(ROOT, 'index.html')
idx = open(idx_path, encoding='utf8').read()
if '<!-- PRODUCTS:START -->' in idx:
    idx = re.sub(r'<!-- PRODUCTS:START -->.*?<!-- PRODUCTS:END -->', lambda m: section, idx, flags=re.S)
else:
    idx = idx.replace('<!-- HOW I WORK -->', section + '\n\n  <!-- HOW I WORK -->')
open(idx_path, 'w', encoding='utf8').write(idx)
print(f'Built {len(products)} product pages and updated index.html')
