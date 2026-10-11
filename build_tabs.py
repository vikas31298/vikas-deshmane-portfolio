"""Render the Agentic AI Architecture and Product Research tabs for product pages.

Content lives in product_tabs.json, keyed by product slug. A product without an
"agentic" or "research" entry simply does not get that tab.
"""
import html, json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
e = html.escape

NAVY, GOLD, INK, MUTED, LINE, CARD, CREAM = '#1f3a5f', '#b4832e', '#141c2b', '#5b6475', '#d9dde4', '#ffffff', '#f3f0ea'


def load():
    path = os.path.join(ROOT, 'product_tabs.json')
    return json.load(open(path, encoding='utf8')) if os.path.exists(path) else {}


def wrap(text, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f'{cur} {w}'.strip()
    if cur:
        lines.append(cur)
    return lines


def svg_text(x, y, lines, size, color, weight=500, anchor='middle', lh=None):
    lh = lh or size * 1.3
    y0 = y - (len(lines) - 1) * lh / 2
    spans = ''.join(f'<tspan x="{x}" y="{y0 + i * lh:.1f}">{e(l)}</tspan>' for i, l in enumerate(lines))
    return (f'<text font-family="Inter, Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}" dominant-baseline="middle">{spans}</text>')


def diagram(spec):
    cols = spec['columns']
    n = len(cols)
    M, CW, GAP, NH, NG, TOP = 20, 184, 44, 48, 10, 64
    W = M * 2 + n * CW + (n - 1) * GAP
    rows = max(len(c['nodes']) for c in cols)
    body_h = rows * NH + (rows - 1) * NG
    col_h = TOP + body_h + 20
    bands = spec.get('bands', [])
    BH = 76
    H = col_h + (40 + BH if bands else 0) + 24

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="End-to-end agentic AI architecture">',
           f'<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="{GOLD}"/></marker></defs>']

    for i, c in enumerate(cols):
        x = M + i * (CW + GAP)
        hi = c.get('highlight')
        out.append(f'<rect x="{x}" y="10" width="{CW}" height="{col_h}" rx="16" fill="{NAVY if hi else CREAM}" stroke="{NAVY if hi else LINE}"/>')
        out.append(svg_text(x + CW / 2, 40, wrap(c['title'].upper(), 22), 11, GOLD if not hi else '#f0d79a', 700, lh=14))
        k = len(c['nodes'])
        start = TOP + (body_h - (k * NH + (k - 1) * NG)) / 2
        for j, node in enumerate(c['nodes']):
            y = start + j * (NH + NG)
            fill = '#ffffff' if not hi else '#2b4d7c'
            stroke = LINE if not hi else '#4a6a95'
            col = INK if not hi else '#ffffff'
            out.append(f'<rect x="{x + 12}" y="{y}" width="{CW - 24}" height="{NH}" rx="10" fill="{fill}" stroke="{stroke}"/>')
            out.append(svg_text(x + CW / 2, y + NH / 2, wrap(node, 22), 12.5, col, 600, lh=15))
        if i < n - 1:
            ay = 10 + col_h / 2
            out.append(f'<line x1="{x + CW + 4}" y1="{ay}" x2="{x + CW + GAP - 4}" y2="{ay}" stroke="{GOLD}" stroke-width="2.5" marker-end="url(#arr)"/>')

    if bands:
        by = col_h + 40
        out.append(svg_text(M, by - 14, ['CROSS-CUTTING CONTROLS'], 11, GOLD, 700, 'start'))
        bw = (W - 2 * M - (len(bands) - 1) * 12) / len(bands)
        for i, b in enumerate(bands):
            x = M + i * (bw + 12)
            out.append(f'<rect x="{x}" y="{by}" width="{bw}" height="{BH}" rx="12" fill="#ffffff" stroke="{LINE}"/>')
            out.append(f'<rect x="{x}" y="{by}" width="5" height="{BH}" rx="2" fill="{GOLD}"/>')
            out.append(svg_text(x + 18, by + 22, [b['title']], 13, NAVY, 700, 'start'))
            out.append(svg_text(x + 18, by + 50, wrap(b['text'], int(bw / 7)), 11.5, MUTED, 500, 'start', lh=15))
    out.append('</svg>')
    return ''.join(out)


def agentic_tab(a):
    flow = ''.join(f'<li>{e(s)}</li>' for s in a['flow'])
    rows = ''.join(f'<tr><td><strong>{e(g["name"])}</strong></td><td>{e(g["role"])}</td><td>{e(g["guard"])}</td></tr>' for g in a['agents'])
    return f"""
  <section class="section section--tight">
    <div class="container">
      <div class="section__head"><p class="eyebrow">Agentic AI architecture</p><h2>End to end, from raw signal to action</h2><p class="section__sub">{e(a['summary'])}</p></div>
      <div class="diagram">{diagram(a)}</div>
      <p class="diagram__hint">Scroll sideways to see the full diagram on small screens.</p>
    </div>
  </section>
  <section class="section section--tight section--alt">
    <div class="container detail">
      <div class="detail__side"><p class="eyebrow">Request lifecycle</p><h2>How one signal moves through the system</h2></div>
      <div class="detail__main"><ol class="numbered">{flow}</ol></div>
    </div>
  </section>
  <section class="section section--tight">
    <div class="container">
      <div class="section__head"><p class="eyebrow">Agent roster</p><h2>Who does what, and what keeps it safe</h2></div>
      <div class="table-wrap"><table class="agents">
        <thead><tr><th>Agent</th><th>Responsibility</th><th>Guardrail</th></tr></thead>
        <tbody>{rows}</tbody>
      </table></div>
    </div>
  </section>"""


def research_tab(r):
    methods = ''.join(f'<li>{e(m)}</li>' for m in r['methods'])
    personas = ''
    for p in r['personas']:
        goals = ''.join(f'<li>{e(g)}</li>' for g in p['goals'])
        pains = ''.join(f'<li>{e(x)}</li>' for x in p['pains'])
        initials = ''.join(w[0] for w in p['name'].split()[:2]).upper()
        end = ' persona--end' if p['type'].lower().startswith('end customer') else ''
        personas += f"""
        <article class="persona{end}">
          <header><span class="persona__avatar">{e(initials)}</span><div><h4>{e(p['name'])}</h4><span class="persona__type">{e(p['type'])}</span></div></header>
          <p class="persona__about">{e(p['about'])}</p>
          <div class="persona__cols">
            <div><h5>Goals</h5><ul>{goals}</ul></div>
            <div><h5>Pain points</h5><ul>{pains}</ul></div>
          </div>
          <p class="persona__needs"><strong>Needs:</strong> {e(p['needs'])}</p>
        </article>"""
    insights = ''.join(f'<div class="insight"><p class="insight__q">{e(i["insight"])}</p><p class="insight__a"><span>Product decision</span>{e(i["decision"])}</p></div>' for i in r['insights'])
    return f"""
  <section class="section section--tight">
    <div class="container">
      <div class="section__head"><p class="eyebrow">Product research</p><h2>Who we built for</h2><p class="section__sub">{e(r['summary'])}</p></div>
      <div class="arch__stack"><span>Research methods</span><ul class="chips">{methods}</ul></div>
    </div>
  </section>
  <section class="section section--tight section--alt">
    <div class="container">
      <div class="section__head"><p class="eyebrow">Personas</p><h2>End users and customers</h2></div>
      <div class="personas">{personas}
      </div>
    </div>
  </section>
  <section class="section section--tight">
    <div class="container">
      <div class="section__head"><p class="eyebrow">Insights to decisions</p><h2>What we learned and what we changed</h2></div>
      <div class="insights">{insights}</div>
    </div>
  </section>"""


def tabs_for(slug):
    """Return (nav_html, extra_panels_html) for a product slug."""
    data = load().get(slug, {})
    tabs = [('overview', 'Overview')]
    panels = ''
    if 'agentic' in data:
        tabs.append(('architecture', 'Agentic AI Architecture'))
        panels += f'<div class="tabpanel" id="tab-architecture" role="tabpanel" hidden>{agentic_tab(data["agentic"])}\n</div>\n'
    if 'research' in data:
        tabs.append(('research', 'Product Research'))
        panels += f'<div class="tabpanel" id="tab-research" role="tabpanel" hidden>{research_tab(data["research"])}\n</div>\n'
    if len(tabs) == 1:
        return '', ''
    buttons = ''.join(
        f'<button class="tabs__btn" role="tab" data-tab="{k}" aria-selected="{"true" if i == 0 else "false"}">{e(label)}</button>'
        for i, (k, label) in enumerate(tabs))
    nav = f'<nav class="tabs" id="productTabs"><div class="container tabs__inner" role="tablist">{buttons}</div></nav>\n'
    return nav, panels
