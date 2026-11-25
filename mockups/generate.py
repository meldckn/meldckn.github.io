"""Generate static HTML mockups of the gallery page (variations A–D).

Run:  python3 mockups/generate.py   (from the repo root)
Then render each mockups/variant-*.html to PNG with headless Chrome.
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
ASSETS = HERE / "assets"
NAME = "Melanie Dickinson"

# Images from the root of Media/Main Gallery (copied/resized into assets/).
# Titles come from the filenames; years are unknown for now, so left blank.
TITLES = {
    "astudyofeyes": "A Study of Eyes",
    "bonespoon": "Bone Spoon",
    "bubbles-10": "Bubbles",
    "bubbles": "Bubbles",
    "column": "Column",
    "cullyrabbit": "Cully Rabbit",
    "cullyturtle-originalpaint": "Cully Turtle (original paint)",
    "cullyturtle-repaint-2": "Cully Turtle",
    "drip1": "Drip I",
    "drip2": "Drip II",
    "fingerpint4": "Fingerprint IV",
    "fingerprint1": "Fingerprint I",
    "fingerprint2": "Fingerprint II",
    "fingerprint3": "Fingerprint III",
    "fingerprint4-2": "Fingerprint IV",
    "fingers": "Fingers",
    "footed1-2": "Footed Bowl I",
    "footed1": "Footed Bowl I",
    "footed2": "Footed Bowl II",
    "spikes": "Spikes",
    "wave": "Wave",
    "woodrabbit": "Wood Rabbit",
}
TITLES.update({
    "cullyturtle-repaint": "Cully Turtle", "wyeastturtle": "Wy'east Turtle",
    "wyeastturtle-6": "Wy'east Turtle (in progress)",
    "cullyrabbit-5": "Cully Rabbit", "cullyrabbit-6": "Cully Rabbit (in progress)",
    "fingers-2": "Fingers", "fingerprint5": "Fingerprint V",
    "drip2-2": "Drip II", "drip2-4": "Drip II",
    "footed1-3": "Footed Bowl", "spiderweb": "Spiderweb", "spiderweb-3": "Spiderweb", "starfield": "Starfield",
    "crow": "Crow", "carrot": "Carrot",
})

# Main section order (reads left-to-right, top-to-bottom in layout B).
# Starfield near the top; Spiderweb well away from it (similar backgrounds);
# Crow, Bone Spoon and Footed Bowl at the bottom.
ORDER = [
    "fingerprint1", "drip1", "starfield", "column", "fingerpint4", "astudyofeyes",
    "spikes", "fingerprint4-2", "fingerprint3", "wave", "spiderweb", "spiderweb-3", "fingers-2", "fingers",
    "fingerprint5", "drip2-2", "drip2-4", "woodrabbit", "carrot",
    "crow", "bonespoon", "footed1-3",
]
# Large concrete sculptures get their own section below the main work.
CONCRETE = [
    "cullyturtle-repaint", "cullyturtle-originalpaint", "wyeastturtle", "wyeastturtle-6",
    "cullyrabbit-5", "cullyrabbit-6", "bubbles",
]
_available = {p.stem for p in ASSETS.glob("*.jpg")}
_main = [s for s in ORDER if s in _available] + sorted(_available - set(ORDER) - set(CONCRETE))


def _pieces(stems):
    return [(TITLES.get(s, s), "", s) for s in stems if s in _available]


PIECES = _pieces(_main + CONCRETE)
SECTIONS = [  # (heading or None, pieces)
    (None, _pieces(_main)),
    ("Large Sculptures", _pieces(CONCRETE)),
]


def sections(container_cls, item_fn):
    """Render each section as its own container, with an optional heading first."""
    out = []
    for label, pieces in SECTIONS:
        items = "".join(item_fn(i, p) for i, p in enumerate(pieces))
        head = f'<h2 class="sec-h">{label}</h2>' if label else ""
        out.append(f'<section class="{container_cls}">{head}{items}</section>')
    return "".join(out)


def ar(stem):
    w, h = Image.open(ASSETS / f"{stem}.jpg").size
    return w / h


def img(stem):
    return f"assets/{stem}.jpg"


BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff;color:#1a1a1a}
body{font-family:var(--font);font-weight:300;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
img{display:block;width:100%}
.sec-h{grid-column:1/-1;column-span:all;width:100%;display:flex;align-items:baseline;gap:14px;
  font-weight:300;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:#1a1a1a;
  padding-bottom:14px;margin-bottom:28px;border-bottom:1px solid #e6e6e6}
.sec-h span{color:#b5b5b5;letter-spacing:.08em}
"""


def page(title, fonts, font_stack, css, body):
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet">
<style>:root{{--font:{font_stack}}}{BASE_CSS}{css}</style>
</head><body>{body}</body></html>"""


def header(extra_cls=""):
    return f"""<header class="hdr {extra_cls}">
  <a class="name" href="#">{NAME}</a>
  <nav><a class="on" href="#">Work</a><a href="#">About</a><a href="#">Contact</a></nav>
</header>"""


# ---------- A: even square grid, captions on hover ----------
def variant_a():
    hovered = "astudyofeyes"
    items = sections("grid", lambda i, p: f"""<a class="tile{' hover' if p[2] == hovered else ''}" href="#"><img src="{img(p[2])}">
<span class="cap"><b>{p[0]}</b><i>{p[1]}</i></span></a>""")
    css = """
.hdr{display:flex;justify-content:space-between;align-items:baseline;padding:44px 56px 56px}
.name{font-size:22px;font-weight:300;letter-spacing:.02em}
nav a{margin-left:32px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#888}
nav a.on{color:#1a1a1a}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;padding:0 56px 96px}
.grid .sec-h{margin-bottom:8px}
.tile{position:relative;aspect-ratio:1;overflow:hidden;background:#f4f4f4}
.tile img{height:100%;object-fit:cover;transition:transform .8s cubic-bezier(.2,.7,.2,1)}
.cap{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;
  padding:22px;background:linear-gradient(transparent 55%,rgba(255,255,255,.92));opacity:0;transition:opacity .5s}
.cap b{font-weight:400;font-size:17px}.cap i{font-style:normal;font-size:13px;color:#777;margin-top:4px}
.tile.hover img{transform:scale(1.04)}.tile.hover .cap{opacity:1}
"""
    body = header() + f'<main>{items}</main>'
    return page(f"{NAME} — A", "family=Jost:wght@300;400", "'Jost',sans-serif", css, body)


# ---------- B: masonry, natural proportions, captions below ----------
def masonry_columns(pieces, n=3, caption=0.12):
    """Place pieces left-to-right into the currently shortest column, so the
    order reads across rows (like the real site will, via a little JS)."""
    cols, heights = [[] for _ in range(n)], [0.0] * n
    for piece in pieces:
        i = heights.index(min(heights))
        cols[i].append(piece)
        heights[i] += 1 / ar(piece[2]) + caption
    return cols


def variant_b():
    def card(p):
        return (f'<a class="card" href="#"><img src="{img(p[2])}">'
                f'<span class="cap">{p[0]}<em>{p[1]}</em></span></a>')

    items = ""
    for label, pieces in SECTIONS:
        cols = "".join(f'<div class="col">{"".join(card(p) for p in c)}</div>'
                       for c in masonry_columns(pieces))
        head = f'<h2 class="sec-h">{label}</h2>' if label else ""
        items += f'<section class="sec">{head}<div class="masonry">{cols}</div></section>'
    css = """
.hdr{display:flex;justify-content:space-between;align-items:center;padding:40px 64px 64px}
.name{font-size:15px;font-weight:400;letter-spacing:.28em;text-transform:uppercase}
nav a{margin-left:36px;font-size:14px;color:#999}
nav a.on{color:#1a1a1a;border-bottom:1px solid #1a1a1a;padding-bottom:3px}
.sec{padding:0 64px 72px}
.sec .sec-h{margin-bottom:36px}
.masonry{display:grid;grid-template-columns:repeat(3,1fr);column-gap:36px;align-items:start}
.card{display:block;margin-bottom:40px}
.cap{display:flex;justify-content:space-between;margin-top:12px;font-size:14px;color:#333}
.cap em{font-style:normal;color:#aaa}
"""
    body = header() + f'<main>{items}</main>'
    return page(f"{NAME} — B", "family=Inter:wght@300;400", "'Inter',sans-serif", css, body)


# ---------- C: fixed sidebar, two airy columns ----------
def variant_c():
    items = sections("grid", lambda i, p: f"""<a class="card" href="#"><div class="frame"><img src="{img(p[2])}"></div>
<span class="cap">{p[0]}{', ' + str(p[1]) if p[1] else ''}</span></a>""")
    css = """
.wrap{display:grid;grid-template-columns:280px 1fr}
.side{position:sticky;top:0;height:100vh;padding:56px 48px;display:flex;flex-direction:column}
.name{font-size:30px;line-height:1.15;font-weight:200}
.role{margin-top:14px;font-size:13px;color:#999;letter-spacing:.04em}
.side nav{margin-top:56px;display:flex;flex-direction:column;gap:14px}
.side nav a{font-size:14px;color:#999;margin:0}
.side nav a.on{color:#1a1a1a}
.side nav a.on::before{content:'';display:inline-block;width:18px;height:1px;background:#1a1a1a;vertical-align:middle;margin-right:10px}
main{padding:56px 72px 32px 24px}
.grid{display:grid;grid-template-columns:1fr 1fr;align-content:start;gap:36px 48px;padding-bottom:136px}
.grid .sec-h{margin-bottom:0}
.card:nth-of-type(even){transform:translateY(64px)}
.frame{aspect-ratio:4/5;overflow:hidden;background:#f5f5f5}
.frame img{height:100%;object-fit:cover}
.cap{display:block;margin-top:14px;font-size:13px;color:#888;letter-spacing:.02em}
"""
    body = f"""<div class="wrap"><aside class="side">
  <a class="name" href="#">Melanie<br>Dickinson</a>
  <span class="role">Wood carving &amp; sculpture</span>
  <nav><a class="on" href="#">Work</a><a href="#">About</a><a href="#">Contact</a></nav>
</aside><main>{items}</main></div>"""
    return page(f"{NAME} — C", "family=Manrope:wght@200;300;400", "'Manrope',sans-serif", css, body)


# ---------- D: justified rows, equal heights ----------
def variant_d():
    items = sections("rows", lambda i, p: f"""<a class="j" href="#" style="flex-grow:{ar(p[2])*100:.1f};width:{ar(p[2])*300:.0f}px">
<i style="padding-bottom:{100/ar(p[2]):.2f}%"></i><img src="{img(p[2])}"></a>""")
    css = """
.hdr{display:flex;justify-content:space-between;align-items:baseline;padding:36px 40px 40px}
.name{font-size:20px;font-weight:300}
.name small{font-size:13px;color:#aaa;margin-left:14px}
nav a{margin-left:28px;font-size:14px;color:#999}
nav a.on{color:#1a1a1a}
.rows{display:flex;flex-wrap:wrap;gap:10px;padding:0 40px 64px}
.rows .sec-h{margin-bottom:8px}
.rows::after{content:'';flex-grow:1000000}
.j{position:relative;display:block;background:#f4f4f4}
.j i{display:block}
.j img{position:absolute;inset:0;height:100%;object-fit:cover}
"""
    body = header().replace(f">{NAME}<", f">{NAME}<small>sculpture</small><") + f'<main>{items}</main>'
    return page(f"{NAME} — D", "family=Outfit:wght@300;400", "'Outfit',sans-serif", css, body)


if __name__ == "__main__":
    for key, fn in dict(a=variant_a, b=variant_b, c=variant_c, d=variant_d).items():
        (HERE / f"variant-{key}.html").write_text(fn())
        print("wrote", f"variant-{key}.html")
