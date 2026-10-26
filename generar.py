"""Genera los gráficos del perfil: assets/avatar.svg, assets/banner.svg.

Misma familia que el logo ZERØ de FrostLayer: trazos rectos, esquinas
cortadas, inclinación y brillo helado. Sin fuentes externas en el logo.
Uso: python3 generar.py && rsvg-convert -w 1024 assets/avatar.svg -o assets/avatar.png
"""

import random
from pathlib import Path

ICE = "#a8dcff"
ACCENT = "#4da3ff"
BG = "#080b10"
OUT = Path(__file__).parent / "assets"


def oct_ring(x, y, w, h, c):
    return (f"M{x+c},{y} L{x+w-c},{y} L{x+w},{y+c} L{x+w},{y+h-c} L{x+w-c},{y+h} "
            f"L{x+c},{y+h} L{x},{y+h-c} L{x},{y+c} Z")


def zero_letters(x0, y0, H=130, Wl=90, gap=34, c=22):
    Z = f'<path d="M{x0},{y0} L{x0+Wl},{y0} L{x0},{y0+H} L{x0+Wl},{y0+H}"/>'
    x = x0 + Wl + gap
    E = (f'<path d="M{x+Wl},{y0} L{x+c},{y0} L{x},{y0+c} L{x},{y0+H-c} L{x+c},{y0+H} L{x+Wl},{y0+H}"/>'
         f'<path d="M{x},{y0+H/2} L{x+Wl*0.75},{y0+H/2}"/>')
    x += Wl + gap
    R = (f'<path d="M{x},{y0+H} L{x},{y0} L{x+Wl-c},{y0} L{x+Wl},{y0+c} L{x+Wl},{y0+H/2-c} '
         f'L{x+Wl-c},{y0+H/2} L{x},{y0+H/2}"/>'
         f'<path d="M{x+Wl*0.45},{y0+H/2} L{x+Wl},{y0+H}"/>')
    x += Wl + gap
    O = f'<path d="{oct_ring(x, y0, Wl, H, c)}"/>'
    S = f'<path d="M{x-14},{y0+H+20} L{x+Wl+14},{y0-20}"/>'
    return Z + E + R + O + S


def stroke(sw, color=ICE):
    return (f'fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linejoin="miter" stroke-linecap="butt"')


def avatar():
    S, cx, cy = 512, 256, 256
    w, h, c, over, sw = 170, 240, 42, 38, 18
    x, y = cx - w / 2, cy - h / 2
    body = (f'<path d="{oct_ring(x, y, w, h, c)}"/>'
            f'<path d="M{x-over},{y+h+over} L{x+w+over},{y-over}"/>')
    skew = f'translate({cx},{cy}) skewX(-10) translate({-cx},{-cy})'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
<defs>
  <radialGradient id="bg" cx="50%" cy="45%" r="70%">
    <stop offset="0" stop-color="#132236"/><stop offset="0.55" stop-color="#0b111a"/><stop offset="1" stop-color="{BG}"/>
  </radialGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
</defs>
<rect width="{S}" height="{S}" fill="url(#bg)"/>
<circle cx="{cx}" cy="{cy}" r="214" fill="none" stroke="{ACCENT}" stroke-opacity="0.18" stroke-width="2"/>
<g transform="{skew}">
  <g {stroke(sw)} opacity="0.7" filter="url(#glow)">{body}</g>
  <g {stroke(sw)}>{body}</g>
</g>
</svg>
'''


def banner():
    W, H = 1200, 300
    rnd = random.Random(7)
    flakes = []
    for _ in range(46):
        x = rnd.uniform(0, W)
        r = rnd.choice([1, 1.3, 1.6, 2.2])
        dur = rnd.uniform(9, 18)
        delay = -rnd.uniform(0, dur)
        op = rnd.uniform(0.25, 0.75)
        drift = rnd.choice(["fallA", "fallB"])
        flakes.append(f'<circle class="f" cx="{x:.0f}" cy="-6" r="{r}" opacity="{op:.2f}" '
                      f'style="animation:{drift} {dur:.1f}s linear {delay:.1f}s infinite"/>')
    # Logo de 720×280 escalado y centrado en la mitad superior.
    logo = f'<g transform="skewX(-14) translate(80,0)">{zero_letters(30, 60)}</g>'
    k = 0.72
    tx, ty = W / 2 - 320 * k, 128 - 125 * k
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .glow {{ animation: pulse 4.5s ease-in-out infinite; }}
  .f {{ fill: {ICE}; }}
  @keyframes pulse {{ 0%,100% {{ opacity: .35 }} 50% {{ opacity: .8 }} }}
  @keyframes fallA {{ to {{ transform: translate(24px, {H + 12}px) }} }}
  @keyframes fallB {{ to {{ transform: translate(-18px, {H + 12}px) }} }}
  @media (prefers-reduced-motion: reduce) {{ .glow, .f {{ animation: none }} .f {{ display: none }} }}
  text {{ font-family: ui-monospace, "JetBrains Mono", "SFMono-Regular", Menlo, Consolas, monospace; }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="#0e1724"/>
  </linearGradient>
  <radialGradient id="halo" cx="50%" cy="42%" r="45%">
    <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.16"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="-200" y1="0" x2="0" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#fff" stop-opacity="0.95"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    <animateTransform attributeName="gradientTransform" type="translate"
      values="0 0; 0 0; 1000 0" keyTimes="0; 0.55; 1" dur="7s" repeatCount="indefinite"/>
  </linearGradient>
  <filter id="blur" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="11"/></filter>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#halo)"/>
  <g stroke="{ACCENT}" stroke-opacity="0.06" stroke-width="1">
    {''.join(f'<path d="M{x},0 L{x-170},{H}"/>' for x in range(60, W + 200, 70))}
  </g>
  {''.join(flakes)}
  <g transform="translate({tx:.1f},{ty:.1f}) scale({k})">
    <g class="glow" {stroke(16)} filter="url(#blur)">{logo}</g>
    <g {stroke(16)}>{logo}</g>
    <g {stroke(16, "url(#shine)")} opacity="0.55">{logo}</g>
  </g>
  <text x="{W/2}" y="246" text-anchor="middle" fill="#7f97b2" font-size="17" letter-spacing="6">DATA · AI · LINUX · HOMELAB</text>
  <path d="M{W/2-60},266 L{W/2+60},266" stroke="{ACCENT}" stroke-opacity="0.5" stroke-width="2"/>
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="#1c2a3a"/>
</svg>
'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "avatar.svg").write_text(avatar(), encoding="utf-8")
    (OUT / "banner.svg").write_text(banner(), encoding="utf-8")
