"""Build the three SVG assets and dependency-free web component."""
from pathlib import Path
import json
import math
import re

from motifs import SUN, MOON

ROOT = Path(__file__).resolve().parents[1]
RADIUS = 194


def f(value):
    return f"{0 if abs(value) < 0.00005 else value:.4f}".rstrip("0").rstrip(".") or "0"


def defs():
    return '''<defs>
  <linearGradient id="rim" x1="0" y1="0" x2=".85" y2="1">
    <stop stop-color="#fff3c6"/><stop offset=".17" stop-color="#d9b566"/>
    <stop offset=".36" stop-color="#76501e"/><stop offset=".49" stop-color="#f8e6a8"/>
    <stop offset=".7" stop-color="#d3aa57"/><stop offset=".87" stop-color="#76521f"/><stop offset="1" stop-color="#e4bf72"/>
  </linearGradient>
  <radialGradient id="field" cx=".34" cy=".23" r=".91">
    <stop stop-color="#e8ce8b"/><stop offset=".4" stop-color="#c6a05b"/>
    <stop offset=".73" stop-color="#b28540"/><stop offset="1" stop-color="#e0ba6c"/>
  </radialGradient>
  <linearGradient id="relief" x1=".15" y1="0" x2=".85" y2="1">
    <stop stop-color="#fff0ba"/><stop offset=".28" stop-color="#e5c786"/><stop offset=".56" stop-color="#c5954b"/><stop offset=".8" stop-color="#b18037"/><stop offset="1" stop-color="#f2d992"/>
  </linearGradient>
  <linearGradient id="reliefDark" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#bc914a"/><stop offset="1" stop-color="#775322"/></linearGradient>
  <linearGradient id="fineGold" x1="0" y1="0" x2=".7" y2="1"><stop stop-color="#fff3c4"/><stop offset=".5" stop-color="#bd944c"/><stop offset="1" stop-color="#f4d790"/></linearGradient>
  <linearGradient id="recess" x1="0" y1="0" x2=".6" y2="1"><stop stop-color="#5f401c"/><stop offset="1" stop-color="#b99049"/></linearGradient>
  <linearGradient id="edgeGold" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#573711"/><stop offset=".22" stop-color="#c09a52"/><stop offset=".48" stop-color="#e9d293"/><stop offset=".65" stop-color="#957037"/><stop offset="1" stop-color="#503313"/></linearGradient>
  <linearGradient id="shine" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff9d6" stop-opacity=".25"/><stop offset=".4" stop-color="#fff9d6" stop-opacity="0"/><stop offset=".64" stop-color="#4c3010" stop-opacity=".08"/><stop offset="1" stop-color="#fff0ba" stop-opacity=".12"/></linearGradient>
  <filter id="reliefShadow" x="-15%" y="-15%" width="130%" height="135%" color-interpolation-filters="sRGB"><feDropShadow dx=".8" dy="1.4" stdDeviation=".75" flood-color="#624018" flood-opacity=".85"/></filter>
  <path id="topArc" d="M -148 0 A 148 148 0 0 1 148 0"/>
  <path id="bottomArc" d="M -155 0 A 155 155 0 0 0 155 0"/>
</defs>'''


def coin_face(side):
    """One canonical face, centered at 0,0, with a precisely shared rim."""
    is_front = side == "front"
    ticks = []
    for i in range(144):
        a = i * math.tau / 144
        r1, r2 = 183.5, 188.5
        ticks.append(f'<path d="M {f(r1*math.sin(a))} {f(r1*math.cos(a))} L {f(r2*math.sin(a))} {f(r2*math.cos(a))}"/>')
    dots = "".join(f'<circle cx="{f(174*math.sin(i*math.tau/96))}" cy="{f(174*math.cos(i*math.tau/96))}" r="1.2"/>' for i in range(96))
    # Deterministic fine lathe lines: vector-only, identical on every export.
    brushed = "".join(f'<circle r="{f(115+i*.68)}"/>' for i in range(79))
    title, bottom = ("SOL • AUREUS", "LIGHT • CHANCE • BEGIN") if is_front else ("LUNA • AUREA", "NIGHT • CHANCE • DREAM")
    art = SUN if is_front else MOON
    return f'''<circle r="194" fill="url(#rim)" stroke="#714b1d" stroke-width="1"/>
<circle r="191.8" fill="none" stroke="#fff1ba" stroke-opacity=".75" stroke-width="1.1"/>
<circle r="185.8" fill="none" stroke="#735023" stroke-width="10"/>
<g stroke="url(#fineGold)" stroke-width="1.3">{''.join(ticks)}</g>
<circle r="180.3" fill="url(#rim)" stroke="#edce83" stroke-width="1"/>
<circle r="176.6" fill="url(#field)" stroke="#6e4e24" stroke-width="1.7"/>
<circle r="173" fill="none" stroke="#f6dfa3" stroke-opacity=".65" stroke-width=".7"/>
<g fill="url(#fineGold)" stroke="#795524" stroke-width=".4">{dots}</g>
<g fill="none" stroke="#f7df9d" stroke-width=".24" opacity=".17">{brushed}</g>
<circle r="133" fill="none" stroke="#7e5c2c" stroke-width=".7"/>
<circle r="131.6" fill="none" stroke="#f0d38c" stroke-width=".65"/>
<circle r="125" fill="none" stroke="#8c6932" stroke-opacity=".5" stroke-width=".5"/>
<g fill="#765021" font-family="Georgia, 'Times New Roman', serif" font-weight="600" text-anchor="middle">
 <text font-size="16" letter-spacing="4"><textPath href="#topArc" startOffset="50%">{title}</textPath></text>
 <text font-size="10.5" letter-spacing="3"><textPath href="#bottomArc" startOffset="50%">{bottom}</textPath></text>
</g>
<g fill="#f3d996" font-family="Georgia, 'Times New Roman', serif" font-weight="600" text-anchor="middle" transform="translate(0 -.65)">
 <text font-size="16" letter-spacing="4"><textPath href="#topArc" startOffset="50%">{title}</textPath></text>
 <text font-size="10.5" letter-spacing="3"><textPath href="#bottomArc" startOffset="50%">{bottom}</textPath></text>
</g>
<g fill="url(#fineGold)" stroke="#805927" stroke-width=".5"><path d="M-158 -5 -155 0 -158 5 -161 0Z"/><path d="M158 -5 161 0 158 5 155 0Z"/></g>
<g filter="url(#reliefShadow)">{art}</g>
<path d="M -24 113 H -9 M 9 113 H 24" stroke="#f1d799" stroke-width=".8"/>
<path d="M 0 109 4 113 0 117 -4 113Z" fill="url(#fineGold)" stroke="#795221" stroke-width=".6"/>
<circle r="179" fill="url(#shine)" pointer-events="none"/>'''


def pose(angle, lift=0, twist=0, scale=1):
    c, s = math.cos(angle), math.sin(angle)
    sx = max(abs(c), .0001)
    if abs(s) < .00001:
        s = 0
        sx = 1
    dx = 7 * s * (1 if c >= 0 else -1)
    rx, half = RADIUS*sx, 7*abs(s)
    edge = f'M {f(-half)} -194 H {f(half)} A {f(rx)} 194 0 0 1 {f(half)} 194 H {f(-half)} A {f(rx)} 194 0 0 1 {f(-half)} -194 Z'
    return {"offset": f"{f(dx)} 0", "squash": f"{f(sx)} 1", "edge": edge,
            "front": "visible" if c >= 0 else "hidden", "back": "hidden" if c >= 0 else "visible",
            "lift": f"0 {f(lift)}", "twist": f(twist), "scale": f(scale)}


def ease(t):
    return t*t*t*(t*(t*6-15)+10)


def loop_pose(t):
    if t <= .08 or t >= .93:
        return pose(0)
    if .43 <= t <= .58:
        return pose(math.pi)
    second = t > .58
    p = (t - (.58 if second else .08)) / .35
    flight = math.sin(math.pi*p)
    return pose((math.pi if second else 0) + 5*math.pi*ease(p), -34*flight, 6*math.sin(math.tau*p)*flight, 1+.035*flight)


def animation(attribute, values, discrete=False):
    keytimes = ";".join(f(i/360) for i in range(361))
    return f'<animate attributeName="{attribute}" dur="6.4s" repeatCount="indefinite" calcMode="{"discrete" if discrete else "linear"}" keyTimes="{keytimes}" values="{";".join(values)}"/>'


def svg(side="front", animated=False, runtime=False):
    p = pose(0 if side == "front" else math.pi)
    samples = [loop_pose(i/360) for i in range(361)] if animated else []
    def anim(attr, key, discrete=False):
        return animation(attr, [v[key] for v in samples], discrete) if animated else ""
    def anim_transform(kind, key):
        if not animated:
            return ""
        return animation("transform", [v[key] for v in samples]).replace('<animate ', f'<animateTransform type="{kind}" ')
    reeds = " ".join(f'M -220 {f(RADIUS*math.sin(i*math.pi/80))} H 220' for i in range(-39,40))
    title = 'Aurum · 日曜正面' if side == 'front' else 'Aurum · 月相反面'
    if animated:
        title = 'Aurum · 日月硬币翻转动画'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" width="512" height="512" role="img" aria-labelledby="coinTitle coinDesc">
<title id="coinTitle">{title}</title>
<desc id="coinDesc">日曜与月相双面金属硬币，精细齿边、同心雕刻和金色浮雕。{'连续翻转，依次停留在正面与反面，首尾无缝循环。' if animated else '透明背景。'}</desc>
{defs()}
<defs><clipPath id="edgeClip"><path data-edge-clip="" d="{p['edge']}">{anim('d','edge')}</path></clipPath></defs>
<g transform="translate(256 256)"><g data-lift="" transform="translate(0 0)">{anim_transform('translate','lift')}
<g data-twist="" transform="rotate(0)">{anim_transform('rotate','twist')}
<g data-scale="" transform="scale(1)">{anim_transform('scale','scale')}
<g data-edge=""><path data-edge-path="" d="{p['edge']}" fill="url(#edgeGold)" stroke="#916a31" stroke-width=".5">{anim('d','edge')}</path>
<g clip-path="url(#edgeClip)"><path d="{reeds}" stroke="#4a2c0c" stroke-opacity=".7" stroke-width="1.1"/><path d="{reeds}" transform="translate(0 .9)" stroke="#f5d896" stroke-opacity=".6" stroke-width=".65"/></g></g>
<g data-face="front" visibility="{p['front']}">{anim('visibility','front',True)}<g data-offset="" transform="translate({p['offset']})">{anim_transform('translate','offset')}<g data-squash="" transform="scale({p['squash']})">{anim_transform('scale','squash')}{coin_face('front')}</g></g></g>
<g data-face="back" visibility="{p['back']}">{anim('visibility','back',True)}<g data-offset="" transform="translate({p['offset']})">{anim_transform('translate','offset')}<g data-squash="" transform="scale({p['squash']})">{anim_transform('scale','squash')}{coin_face('back')}</g></g></g>
</g></g></g></g>
</svg>'''


def build():
    (ROOT / "assets").mkdir(exist_ok=True)
    for filename, side, moving in [("coin-front.svg","front",False),("coin-back.svg","back",False),("coin-flip.svg","front",True)]:
        (ROOT / "assets" / filename).write_text(svg(side, moving))
    template = (ROOT / "src" / "component.js").read_text()
    (ROOT / "coin-simulator.js").write_text(template.replace("__COIN_SVG__", json.dumps(svg(), ensure_ascii=False)))
    # Offline demo: the deliverable opens directly from disk, with no local server required.
    html = (ROOT / "src" / "demo.html").read_text()
    html = html.replace("<!-- INLINE_COMPONENT -->", '<script>' + (ROOT / "coin-simulator.js").read_text() + '</script>')
    for name in ["front", "back", "flip"]:
        content = svg("back" if name == "back" else "front", name == "flip")
        # Prefix IDs so inline asset previews cannot resolve another coin's defs.
        ids = re.findall(r'\bid="([^"]+)"', content)
        for id_ in ids:
            content = content.replace(f'id="{id_}"', f'id="preview-{name}-{id_}"').replace(f'#{id_}"', f'#preview-{name}-{id_}"').replace(f'#{id_})', f'#preview-{name}-{id_})')
        content = content.replace('aria-labelledby="coinTitle coinDesc"', f'aria-labelledby="preview-{name}-coinTitle preview-{name}-coinDesc"')
        html = html.replace(f'<!-- PREVIEW_{name.upper()} -->', content)
    (ROOT / "index.html").write_text(html)
    print('Built 3 SVGs, coin-simulator.js, and standalone index.html')


if __name__ == '__main__':
    build()
