"""Generate themed SVG cover images for each product into assets/products/<slug>.svg.

Run:  python build_covers.py   (build_products.py runs this automatically)
To use a real screenshot instead, set "image": "assets/products/your-file.jpg" on that product in products.json.
"""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'assets', 'products')
os.makedirs(OUT, exist_ok=True)

NAVY, NAVY2, GOLD, CREAM, MINT = '#1f3a5f', '#14263f', '#f0d79a', '#fbfaf7', '#8fd3c7'
W, H = 800, 450


def frame(inner, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(label)}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY2}"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity="0.05"/>
    </pattern>
    <radialGradient id="glow" cx="0.85" cy="0.1" r="0.7">
      <stop offset="0" stop-color="{GOLD}" stop-opacity="0.22"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
  {inner}
</svg>
'''


def card(x, y, w, h, style=''):
    style = style or 'fill="#ffffff" fill-opacity="0.07"'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" {style} stroke="#ffffff" stroke-opacity="0.14"/>'


def txt(x, y, s, size=14, color=CREAM, weight=600, anchor='start', op=1):
    return f'<text x="{x}" y="{y}" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" fill-opacity="{op}" text-anchor="{anchor}">{html.escape(s)}</text>'


def cx_anomaly():
    # Dashboard with NPS trend line, anomaly spike, routed alerts
    pts = [(90, 330), (150, 310), (210, 318), (270, 290), (330, 300), (390, 250), (450, 262), (510, 225), (570, 205), (630, 180), (690, 150)]
    line = ' '.join(f'{x},{y}' for x, y in pts)
    area = f'90,370 {line} 690,370'
    g = card(60, 60, 680, 330)
    g += txt(90, 100, 'NPS TREND', 12, GOLD, 700)
    g += txt(90, 130, '58 → 70+', 28, CREAM, 700)
    g += f'<polygon points="{area}" fill="{GOLD}" fill-opacity="0.10"/>'
    g += f'<polyline points="{line}" fill="none" stroke="{GOLD}" stroke-width="3" stroke-linejoin="round"/>'
    for x, y in pts:
        g += f'<circle cx="{x}" cy="{y}" r="4" fill="{NAVY2}" stroke="{GOLD}" stroke-width="2"/>'
    # anomaly marker
    g += f'<circle cx="390" cy="250" r="16" fill="none" stroke="{MINT}" stroke-width="2" stroke-dasharray="4 4"/>'
    g += card(430, 84, 280, 64, f'fill="{MINT}" fill-opacity="0.12"')
    g += txt(448, 110, 'Anomaly detected', 14, MINT, 700)
    g += txt(448, 132, 'Routed to Ops · Theme: handover delays', 12, CREAM, 500, op=0.75)
    g += f'<path d="M406 238 L460 148" stroke="{MINT}" stroke-width="1.5" stroke-dasharray="4 4"/>'
    return frame(g, 'AI customer-experience analytics dashboard')


def event_platform():
    # Kafka event bus with microservices
    g = txt(400, 70, 'APPLICATION → DISBURSAL', 12, GOLD, 700, 'middle')
    g += f'<rect x="80" y="205" width="640" height="40" rx="20" fill="{GOLD}" fill-opacity="0.18" stroke="{GOLD}" stroke-opacity="0.6"/>'
    g += txt(400, 231, 'Kafka event stream', 14, GOLD, 700, 'middle')
    for i in range(14):
        cx = 110 + i * 45
        g += f'<circle cx="{cx}" cy="225" r="3" fill="{GOLD}" fill-opacity="0.8"/>'
    top = ['Intake', 'Validation', 'KYC · Fraud', 'Decisioning']
    bot = ['Authorization', 'Disbursal', 'Servicing', 'Routing']
    for i, n in enumerate(top):
        x = 95 + i * 160
        g += card(x, 100, 130, 60)
        g += txt(x + 65, 136, n, 14, CREAM, 600, 'middle')
        g += f'<line x1="{x + 65}" y1="160" x2="{x + 65}" y2="205" stroke="#ffffff" stroke-opacity="0.3" stroke-width="2"/>'
    for i, n in enumerate(bot):
        x = 95 + i * 160
        g += card(x, 290, 130, 60)
        g += txt(x + 65, 326, n, 14, CREAM, 600, 'middle')
        g += f'<line x1="{x + 65}" y1="245" x2="{x + 65}" y2="290" stroke="#ffffff" stroke-opacity="0.3" stroke-width="2"/>'
    g += txt(400, 400, '50K+ applications / day  ·  99.95% uptime', 14, CREAM, 600, 'middle', 0.8)
    return frame(g, 'Event-driven transaction platform architecture')


def llm_quality():
    # Pipeline with quality gates
    g = txt(400, 70, 'LLM RELEASE PIPELINE', 12, GOLD, 700, 'middle')
    stages = [('Build', ''), ('Accuracy', '✓'), ('Hallucination', '✓'), ('Safety', '✓'), ('Deploy', '')]
    for i, (n, mark) in enumerate(stages):
        x = 70 + i * 140
        gate = mark != ''
        plain = 'fill="#ffffff" fill-opacity="0.07" stroke="#ffffff" stroke-opacity="0.14"'
        fill = f'fill="{MINT}" fill-opacity="0.14" stroke="{MINT}" stroke-opacity="0.6"' if gate else plain
        g += f'<rect x="{x}" y="150" width="110" height="110" rx="14" {fill}/>'
        if gate:
            g += f'<circle cx="{x + 55}" cy="190" r="18" fill="{MINT}" fill-opacity="0.25"/>'
            g += txt(x + 55, 197, '✓', 20, MINT, 700, 'middle')
        else:
            g += f'<circle cx="{x + 55}" cy="190" r="18" fill="#ffffff" fill-opacity="0.08"/>'
        g += txt(x + 55, 240, n, 13, CREAM, 600, 'middle')
        if i < len(stages) - 1:
            g += f'<path d="M{x + 112} 205 L{x + 136} 205" stroke="{GOLD}" stroke-width="2.5" marker-end="url(#a)"/>'
    g = g.replace(txt(400, 70, 'LLM RELEASE PIPELINE', 12, GOLD, 700, 'middle'),
                  f'<defs><marker id="a" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{GOLD}"/></marker></defs>' + txt(400, 70, 'LLM RELEASE PIPELINE', 12, GOLD, 700, 'middle'), 1)
    for i, (v, l) in enumerate([('94%', 'caught pre-deploy'), ('−52%', 'inference cost'), ('<3s', 'answer latency')]):
        x = 130 + i * 210
        g += txt(x, 330, v, 30, GOLD, 700, 'middle')
        g += txt(x, 356, l, 13, CREAM, 500, 'middle', 0.75)
    return frame(g, 'LLM quality-gate pipeline')


def lending_growth():
    # Rising bars + rule engine chips
    g = txt(80, 80, 'LENDING PORTFOLIO', 12, GOLD, 700)
    g += txt(80, 112, '₹800Cr → ₹2,100Cr', 26, CREAM, 700)
    vals = [800, 950, 1150, 1400, 1700, 2100]
    for i, v in enumerate(vals):
        h = v / 2100 * 220
        x = 90 + i * 62
        g += f'<rect x="{x}" y="{380 - h}" width="40" height="{h}" rx="6" fill="{GOLD}" fill-opacity="{0.35 + i * 0.12:.2f}"/>'
    g += f'<line x1="80" y1="380" x2="460" y2="380" stroke="#ffffff" stroke-opacity="0.25"/>'
    g += card(500, 90, 230, 290)
    g += txt(520, 122, 'RULE ENGINE', 12, GOLD, 700)
    for i, r in enumerate(['Validation', 'Credit evaluation', 'Risk scoring', 'Approval automation', 'Partner config']):
        y = 145 + i * 44
        g += f'<rect x="520" y="{y}" width="190" height="32" rx="8" fill="#ffffff" fill-opacity="0.08"/>'
        g += f'<circle cx="538" cy="{y + 16}" r="5" fill="{MINT}"/>'
        g += txt(552, y + 21, r, 13, CREAM, 500)
    return frame(g, 'Lending portfolio growth and rule engine')


def nlp_routing():
    # Incoming messages classified and routed
    g = txt(400, 64, 'CLASSIFY  →  ROUTE  →  RESOLVE', 12, GOLD, 700, 'middle')
    msgs = ['Where is my payout?', 'KYC document upload', 'Order not executed', 'Change bank account']
    for i, m in enumerate(msgs):
        y = 100 + i * 72
        g += f'<rect x="60" y="{y}" width="210" height="46" rx="14" fill="#ffffff" fill-opacity="0.09" stroke="#ffffff" stroke-opacity="0.15"/>'
        g += txt(78, y + 28, m, 13, CREAM, 500)
        g += f'<path d="M272 {y + 23} C 320 {y + 23}, 330 225, 350 225" fill="none" stroke="{GOLD}" stroke-opacity="0.5" stroke-width="1.5"/>'
    g += f'<circle cx="400" cy="225" r="52" fill="{GOLD}" fill-opacity="0.16" stroke="{GOLD}" stroke-opacity="0.7"/>'
    g += txt(400, 222, 'NLP', 18, GOLD, 700, 'middle')
    g += txt(400, 242, 'classifier', 12, CREAM, 500, 'middle', 0.8)
    outs = [('Auto-resolved', MINT), ('Payments team', CREAM), ('KYC · 30 min', MINT), ('Trading desk', CREAM)]
    for i, (o, c) in enumerate(outs):
        y = 100 + i * 72
        g += f'<path d="M452 225 C 470 225, 480 {y + 23}, 528 {y + 23}" fill="none" stroke="{GOLD}" stroke-opacity="0.5" stroke-width="1.5"/>'
        g += f'<rect x="530" y="{y}" width="210" height="46" rx="14" fill="{c}" fill-opacity="0.12" stroke="{c}" stroke-opacity="0.4"/>'
        g += txt(548, y + 28, o, 13, c, 600)
    return frame(g, 'NLP query classification and routing')


def edtech_funnel():
    # Funnel discover → purchase → serve
    g = txt(80, 80, 'LEARNER JOURNEY', 12, GOLD, 700)
    g += txt(80, 112, '+50% completion efficiency', 24, CREAM, 700)
    steps = [('Discover', 440), ('Evaluate', 380), ('Purchase', 320), ('Learn', 270), ('AI evaluation', 230)]
    for i, (n, w) in enumerate(steps):
        y = 145 + i * 50
        x = 80 + (440 - w) / 2
        g += f'<rect x="{x}" y="{y}" width="{w}" height="40" rx="10" fill="{GOLD}" fill-opacity="{0.18 + i * 0.12:.2f}"/>'
        g += txt(300, y + 26, n, 14, CREAM, 600, 'middle')
    g += card(560, 145, 180, 90)
    g += txt(650, 185, '5K+', 28, GOLD, 700, 'middle')
    g += txt(650, 210, 'concurrent users', 12, CREAM, 500, 'middle', 0.8)
    g += card(560, 255, 180, 90)
    g += txt(650, 295, '95%', 28, MINT, 700, 'middle')
    g += txt(650, 320, 'AI relevance accuracy', 12, CREAM, 500, 'middle', 0.8)
    return frame(g, 'EdTech learner journey funnel')


THEMES = {
    'cx-anomaly-platform': cx_anomaly,
    'dhani-transaction-platform': event_platform,
    'llm-quality-platform': llm_quality,
    'dmi-loan-management': lending_growth,
    'angel-one-servicing-ai': nlp_routing,
    'onyourrank-edtech': edtech_funnel,
}


def _wrap(text, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f'{cur} {w}'.strip()
    return lines + ([cur] if cur else [])


def generic(p):
    # Category label, product name and three headline metrics as tiles
    g = txt(70, 90, p['category'].upper(), 13, GOLD, 700)
    for i, line in enumerate(_wrap(p['name'], 30)[:3]):
        g += txt(70, 140 + i * 40, line, 32, CREAM, 700)
    for i, m in enumerate(p['hero_metrics'][:3]):
        x = 70 + i * 225
        g += card(x, 290, 205, 100)
        g += txt(x + 18, 332, m['value'], 22 if len(m['value']) < 12 else 17, GOLD, 700)
        for j, line in enumerate(_wrap(m['label'], 28)[:2]):
            g += txt(x + 18, 358 + j * 16, line, 12, CREAM, 500, op=0.8)
    g += f'<circle cx="700" cy="120" r="70" fill="none" stroke="{GOLD}" stroke-opacity="0.35" stroke-width="2"/>'
    g += f'<circle cx="700" cy="120" r="44" fill="{GOLD}" fill-opacity="0.12"/>'
    g += f'<circle cx="700" cy="120" r="8" fill="{GOLD}"/>'
    return frame(g, p['name'])


def build():
    products = json.load(open(os.path.join(ROOT, 'products.json'), encoding='utf8'))
    for p in products:
        if p.get('image'):
            continue
        fn = THEMES.get(p['slug'])
        svg = fn() if fn else generic(p)
        with open(os.path.join(OUT, p['slug'] + '.svg'), 'w', encoding='utf8') as f:
            f.write(svg)
    print(f'Built covers in {OUT}')


if __name__ == '__main__':
    build()
