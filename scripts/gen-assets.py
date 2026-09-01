"""Render the favicon mark and the OG cards with headless Chrome.

Run from anywhere:  python3 scripts/gen-assets.py
Rerun it after changing an app icon, accent, or card line. Outputs land in
assets/og/ and assets/. Requires Google Chrome; nothing else.
"""
import base64, pathlib, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TMP = pathlib.Path(tempfile.mkdtemp(prefix='kstech-cards-'))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

FRAUNCES = b64(ROOT / 'assets/fonts/fraunces-latin-63f165.woff2')
SANS = b64(ROOT / 'assets/fonts/instrument-sans-latin-e190a6.woff2')
MONO = b64(ROOT / 'assets/fonts/spline-sans-mono-latin-53329b.woff2')
SQUIRCLE = base64.b64encode((ROOT / 'assets/squircle.svg').read_bytes()).decode()

FONTS = f"""
@font-face {{ font-family:'Fraunces'; font-weight:430;
  src:url(data:font/woff2;base64,{FRAUNCES}) format('woff2'); }}
@font-face {{ font-family:'Fraunces'; font-weight:560;
  src:url(data:font/woff2;base64,{FRAUNCES}) format('woff2'); }}
@font-face {{ font-family:'Instrument Sans'; font-weight:400;
  src:url(data:font/woff2;base64,{SANS}) format('woff2'); }}
@font-face {{ font-family:'Spline Sans Mono'; font-weight:400;
  src:url(data:font/woff2;base64,{MONO}) format('woff2'); }}
"""

BASE = """
  *{box-sizing:border-box;margin:0;padding:0}
  :root{--ink:#0F0D0B;--card:#161311;--bone:#EAE5DB;--mist:#938C82;--line:#26221E}
  html,body{width:%(w)spx;height:%(h)spx;overflow:hidden}
  body{background:var(--ink);color:var(--bone);
       font-family:'Instrument Sans',sans-serif;-webkit-font-smoothing:antialiased;
       position:relative}
  .glow{position:absolute;inset:0;
        background:radial-gradient(60%% 90%% at 18%% 12%%,
          color-mix(in srgb, var(--accent) 22%%, transparent) 0%%, transparent 70%%)}
"""

def shot(name, html, w, h, out):
    f = TMP / f'{name}.html'
    f.write_text(html)
    subprocess.run([
        CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
        f'--window-size={w},{h}', '--default-background-color=00000000',
        '--virtual-time-budget=3000',
        f'--screenshot={out}', f'file://{f}',
    ], check=True, capture_output=True)
    print('  wrote', out)


def og_card(name, icon_b64, title, line, accent, w=1200, h=630):
    icon = (f'<div class="icon" style="background-image:url(data:image/png;base64,{icon_b64})"></div>'
            if icon_b64 else '')
    return f"""<!doctype html><meta charset="utf-8"><style>{FONTS}{BASE % {'w': w, 'h': h}}
  body{{--accent:{accent};padding:78px 84px;display:flex;flex-direction:column;
        justify-content:space-between}}
  .top{{display:flex;align-items:center;gap:38px;position:relative}}
  .icon{{width:156px;height:156px;background-size:cover;flex:none;
        -webkit-mask-image:url(data:image/svg+xml;base64,{SQUIRCLE});
        -webkit-mask-size:100% 100%;mask-image:url(data:image/svg+xml;base64,{SQUIRCLE});
        mask-size:100% 100%}}
  h1{{font-family:'Fraunces',serif;font-weight:430;font-size:82px;line-height:1;
      letter-spacing:-.015em}}
  p{{font-size:31px;line-height:1.42;color:var(--mist);max-width:24ch;position:relative}}
  .foot{{font-family:'Spline Sans Mono',monospace;font-size:19px;letter-spacing:.22em;
         text-transform:uppercase;color:var(--mist);position:relative}}
  .foot b{{color:var(--accent);font-weight:400}}
</style><div class="glow"></div>
<div class="top">{icon}<h1>{title}</h1></div>
<p>{line}</p>
<p class="foot"><b>Kstech</b></p>
"""


def site_card(icon_sources, labels, w=1200, h=630):
    tiles = ''.join(
        f'<span style="background-image:url({source})"></span>' if source
        else f'<span class="mono">{label}</span>'
        for source, label in zip(icon_sources, labels))
    return f"""<!doctype html><meta charset="utf-8"><style>{FONTS}{BASE % {'w': w, 'h': h}}
  body{{--accent:#A78BFA;padding:82px 84px;display:flex;flex-direction:column;
        justify-content:space-between}}
  .brand{{font-family:'Spline Sans Mono',monospace;font-size:18px;letter-spacing:.14em;
      color:var(--mist);position:relative}}
  h1{{font-family:'Fraunces',serif;font-weight:430;font-size:116px;
      line-height:.9;letter-spacing:-.05em;position:relative;margin-top:22px;
      display:flex;align-items:flex-start;gap:20px}}
  h1 small{{font-family:'Spline Sans Mono',monospace;font-size:18px;font-weight:400;
      letter-spacing:.14em;color:var(--mist);margin-top:24px}}
  .row{{display:flex;gap:26px;position:relative}}
  .row span{{width:104px;height:104px;background-size:cover;display:grid;place-items:center;
    -webkit-mask-image:url(data:image/svg+xml;base64,{SQUIRCLE});-webkit-mask-size:100% 100%;
    mask-image:url(data:image/svg+xml;base64,{SQUIRCLE});mask-size:100% 100%}}
  .row span.mono{{background:var(--card);color:#C8925B;font-family:'Fraunces',serif;
    font-size:44px}}
</style><div class="glow"></div>
<div><p class="brand">Kstech</p><h1>Apps <small>08</small></h1></div>
<div class="row">{tiles}</div>
"""


def favicon(size):
    return f"""<!doctype html><meta charset="utf-8"><style>{FONTS}
  *{{margin:0;padding:0}}
  html,body{{width:{size}px;height:{size}px;overflow:hidden}}
  body{{background:#0F0D0B;display:grid;place-items:center}}
  span{{font-family:'Fraunces',serif;font-weight:560;font-style:italic;
        font-size:{round(size*0.74)}px;line-height:1;color:#EAE5DB;
        transform:translate({size*-0.035}px,{size*-0.02}px)}}
</style><span>K</span>
"""


APPS = [
    ('pacingguard', 'Pacing Guard',
     'Timed GO and REST intervals with voice cues and heart-rate monitoring.', '#4D94E8'),
    ('respirix', 'Respirix',
     'Real-time HRV biofeedback and resonance breathing from a Bluetooth chest strap.', '#3B82F6'),
    ('lull', 'Lull',
     'White noise, nature sounds and ambient mixes that play all night.', '#C8925B'),
    ('spacesift', 'SpaceSift',
     'Finds duplicates, blurry shots, old screenshots and large videos on your device.', '#D89878'),
    ('promptuary', 'Promptuary',
     'Reusable AI prompts, fragments and chains, one shortcut away.', '#A78BFA'),
]

if __name__ == '__main__':
    icons = {}
    for slug, *_ in APPS:
        p = ROOT / slug / 'assets/app-icon.png'
        icons[slug] = b64(p) if p.exists() else None

    site_icon_paths = {
        'rouse': ROOT / 'assets/apps/rouse.png',
        'lull': ROOT / 'assets/apps/lull.png',
        'skyhop': ROOT / 'assets/apps/skyhop.png',
        'attune': ROOT / 'assets/apps/attune.svg',
    }
    site_icons = {
        slug: f'data:{"image/svg+xml" if path.suffix.lower() == ".svg" else "image/png"};base64,{b64(path)}'
        if path.exists() else None
        for slug, path in site_icon_paths.items()
    }

    (ROOT / 'assets/og').mkdir(parents=True, exist_ok=True)
    print('OG cards:')
    site_slugs = ['spacesift', 'respirix', 'promptuary', 'rouse', 'lull', 'skyhop', 'pacingguard', 'attune']
    site_labels = ['S', 'R', 'Pr', 'R', 'L', 'S', 'P', 'A']
    legacy_site_icons = {
        slug: f'data:image/png;base64,{icon}' if icon else None
        for slug, icon in icons.items()
    }
    site_sources = {**legacy_site_icons, **site_icons}
    shot('og-site', site_card([site_sources.get(s) for s in site_slugs], site_labels), 1200, 630,
         ROOT / 'assets/og/kstech.png')
    for slug, title, line, accent in APPS:
        shot(f'og-{slug}', og_card(slug, icons[slug], title, line, accent), 1200, 630,
             ROOT / f'assets/og/{slug}.png')

    print('favicons:')
    for size, out in [(180, 'apple-touch-icon.png'), (32, 'favicon-32.png'),
                      (512, 'icon-512.png')]:
        shot(f'fav-{size}', favicon(size), size, size, ROOT / 'assets' / out)
