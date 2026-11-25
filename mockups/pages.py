"""Static mockups of piece-page and About-page layouts (P1–P4, A1–A3).

Run from the repo root:  python3 mockups/pages.py
Writes mockups/piece-*.html and mockups/about-*.html, then renders PNGs with
headless Chrome.
"""
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageChops

HERE = Path(__file__).parent
ROOT = HERE.parent
PIECE_DIR = ROOT / "src" / "work" / "wood-rabbit"
ASSETS = HERE / "assets" / "pages"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

NAME = "Melanie Dickinson"
TITLE = "Wood Rabbit"
FILES = ["cover.jpg"] + [f"woodrabbit-{n}.jpg" for n in range(2, 9)]
TEXT = (
    "<p>Placeholder text about the piece: what it is, how it was made, and "
    "anything you’d like people to know. A short paragraph or two reads best "
    "next to the photos.</p>"
    "<p>A second paragraph could cover the wood, tools or the story behind "
    "the piece.</p>"
)
META = [("Year", "—"), ("Materials", "—"), ("Size", "—")]


def prepare_assets():
    ASSETS.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        out = ASSETS / f
        if not out.exists():
            im = Image.open(PIECE_DIR / f)
            im.thumbnail((1600, 1600))
            im.save(out, quality=85)


def src(f):
    return f"assets/pages/{f}"


BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff;color:#1a1a1a}
body{font-family:'Inter',sans-serif;font-weight:300;-webkit-font-smoothing:antialiased;line-height:1.6}
a{color:inherit;text-decoration:none}
img{display:block}
.hdr{display:flex;justify-content:space-between;align-items:center;padding:40px 64px 48px}
.name{font-size:15px;font-weight:400;letter-spacing:.28em;text-transform:uppercase}
nav a{margin-left:32px;font-size:14px;color:#999}
nav a.on{color:#1a1a1a;border-bottom:1px solid #1a1a1a;padding-bottom:3px}
.back{font-size:13px;color:#999}
h1{font-weight:300;font-size:32px;line-height:1.2;letter-spacing:-.01em}
.meta{font-size:13px}
.meta div{display:flex;gap:16px;padding:7px 0;border-top:1px solid #e8e8e8}
.meta div:last-child{border-bottom:1px solid #e8e8e8}
.meta dt{width:80px;color:#999}
.text{font-size:15px;color:#555}
.text p{margin-bottom:1em}
.label{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#999}
.thumbs{display:flex;gap:10px;align-items:center}
.thumbs img{width:84px;height:84px;object-fit:cover;opacity:.55}
.thumbs img.on{opacity:1;outline:1px solid #1a1a1a;outline-offset:3px}
.arrow{width:36px;height:36px;border:1px solid #ddd;border-radius:50%;display:grid;place-items:center;
  font-size:15px;color:#555;flex:none;background:#fff}
.pn{display:flex;justify-content:space-between;margin:72px 64px 0;padding:24px 0 56px;border-top:1px solid #e8e8e8;font-size:15px}
.pn span{display:block;font-size:12px;color:#999;letter-spacing:.1em;text-transform:uppercase}
.pn .r{text-align:right}
.ph{background:#f1f0ee;display:grid;place-items:center;color:#aaa;font-size:14px;letter-spacing:.08em}
"""


def page(title, css, body, nav_on="Work"):
    # Mockups are rendered as one tall screenshot, so pin vh to a 900px screen.
    css = re.sub(r"(\d+)vh", lambda m: f"{int(m.group(1)) * 9}px", css)
    nav = "".join(f'<a class="{"on" if n == nav_on else ""}" href="#">{n}</a>' for n in ["Work", "About"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400&display=swap" rel="stylesheet">
<style>{BASE_CSS}{css}</style></head><body>
<header class="hdr"><a class="name" href="#">{NAME}</a><nav>{nav}</nav></header>
{body}</body></html>"""


def meta():
    return '<dl class="meta">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in META) + "</dl>"


def thumbs(active=0, arrows=True):
    imgs = "".join(f'<img class="{"on" if i == active else ""}" src="{src(f)}">' for i, f in enumerate(FILES))
    if not arrows:
        return f'<div class="thumbs">{imgs}</div>'
    return f'<div class="thumbs"><span class="arrow">&larr;</span>{imgs}<span class="arrow">&rarr;</span></div>'


PN = '<div class="pn"><a href="#"><span>Previous</span>Drip II</a><a class="r" href="#"><span>Next</span>Carrot</a></div>'


# ---------- P1: centered stage, thumbnails, text below ----------
def piece_1():
    css = """
.stage{display:flex;justify-content:center;padding:0 64px}
.stage img{height:68vh;width:auto}
.strip{display:flex;justify-content:center;margin:28px 0 0}
.below{display:grid;grid-template-columns:1fr 1.4fr;gap:80px;max-width:1040px;margin:72px auto 0;padding:0 64px}
.below h1{margin-bottom:20px}
"""
    body = f"""<div class="stage"><img src="{src(FILES[0])}"></div>
<div class="strip">{thumbs()}</div>
<div class="below"><div><a class="back" href="#">&larr; All work</a><h1 style="margin-top:20px">{TITLE}</h1>{meta()}</div>
<div class="text">{TEXT}</div></div>{PN}"""
    return page("P1", css, body)


# ---------- P2: big photo left, info right, thumbnails under photo ----------
def piece_2():
    css = """
.wrap{display:grid;grid-template-columns:1.9fr 1fr;gap:72px;padding:0 64px;align-items:start}
.photo{background:#f5f5f4;display:flex;justify-content:center;height:72vh}
.photo img{height:100%;width:auto}
.strip{margin-top:20px}
.info{padding-top:8px}
.info h1{margin:20px 0 24px}
.info .meta{margin-bottom:28px}
"""
    body = f"""<div class="wrap"><div><div class="photo"><img src="{src(FILES[0])}"></div>
<div class="strip">{thumbs(arrows=False)}</div></div>
<div class="info"><a class="back" href="#">&larr; All work</a><h1>{TITLE}</h1>{meta()}<div class="text">{TEXT}</div></div></div>{PN}"""
    return page("P2", css, body)


# ---------- P3: title bar, wide photo, carousel of medium photos ----------
def piece_3():
    rail = "".join(f'<img src="{src(f)}">' for f in FILES[1:])
    css = """
.bar{display:flex;justify-content:space-between;align-items:baseline;padding:0 64px 24px}
.bar .sub{font-size:13px;color:#999;letter-spacing:.04em}
.hero{padding:0 64px}
.hero img{width:100%;height:74vh;object-fit:cover}
.rail-head{display:flex;justify-content:space-between;align-items:center;padding:40px 64px 16px}
.rail-head .ctl{display:flex;gap:10px}
.rail{display:flex;gap:16px;padding:0 0 0 64px;overflow:hidden}
.rail img{height:240px;width:auto;flex:none}
.below{max-width:640px;margin:64px auto 0;padding:0 24px}
.below .meta{margin-top:28px}
"""
    body = f"""<div class="bar"><h1>{TITLE}</h1><span class="sub">Year &nbsp;·&nbsp; Materials &nbsp;·&nbsp; Size</span></div>
<div class="hero"><img src="{src(FILES[0])}"></div>
<div class="rail-head"><span class="label">More photos &nbsp;7</span><span class="ctl"><span class="arrow">&larr;</span><span class="arrow">&rarr;</span></span></div>
<div class="rail">{rail}</div>
<div class="below"><div class="text">{TEXT}</div>{meta()}</div>{PN}"""
    return page("P3", css, body)


# ---------- P4: slideshow with overlaid arrows + counter, dots ----------
def piece_4():
    dots = "".join(f'<i class="{"on" if i == 0 else ""}"></i>' for i in range(len(FILES)))
    css = """
.show{position:relative;margin:0 64px;background:#f6f6f5;height:74vh;display:flex;justify-content:center}
.show img{height:100%;width:auto}
.show .arrow{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border:0;
  background:rgba(255,255,255,.85);font-size:17px}
.show .l{left:20px}.show .r{right:20px}
.count{position:absolute;right:20px;bottom:16px;font-size:12px;color:#777;background:rgba(255,255,255,.85);padding:3px 10px;letter-spacing:.06em}
.dots{display:flex;gap:10px;justify-content:center;margin-top:18px}
.dots i{width:6px;height:6px;border-radius:50%;background:#d6d6d6}
.dots i.on{background:#1a1a1a}
.strip{display:flex;justify-content:center;margin-top:22px}
.strip .thumbs img{width:64px;height:64px}
.below{max-width:640px;margin:64px auto 0;padding:0 24px;text-align:center}
.below h1{margin-bottom:8px}
.below .sub{font-size:13px;color:#999;margin-bottom:28px}
"""
    body = f"""<div class="show"><img src="{src(FILES[0])}"><span class="arrow l">&larr;</span><span class="arrow r">&rarr;</span><span class="count">1 / 8</span></div>
<div class="strip">{thumbs(arrows=False)}</div>
<div class="below"><h1>{TITLE}</h1><div class="sub">Year &nbsp;·&nbsp; Materials &nbsp;·&nbsp; Size</div><div class="text">{TEXT}</div></div>{PN}"""
    return page("P4", css, body)


BIO = (
    "<p>Placeholder bio. A few sentences about who you are, the materials you "
    "work in, and what draws you to carving and sculpture.</p>"
    "<p>A second paragraph could mention community projects like the Play "
    "Sculptures, exhibitions, or commissions.</p>"
)
CONTACT = """<div class="contact"><span class="label">Contact</span>
<a href="#">meldckn@gmail.com</a><a href="#">Instagram</a></div>"""
ABOUT_CSS = """
.text{font-size:17px;color:#555}
.contact{display:flex;flex-direction:column;gap:8px;font-size:15px}
.contact .label{margin-bottom:6px}
.contact a{border-bottom:1px solid #e8e8e8;align-self:flex-start}
"""


# ---------- A1: portrait photo left, bio + contact right ----------
def about_1():
    css = ABOUT_CSS + """
.wrap{display:grid;grid-template-columns:1fr 1fr;gap:88px;padding:0 64px 96px;align-items:start}
.ph{height:78vh}
.copy{padding-top:24px;max-width:520px}
.copy h1{margin-bottom:28px}
.copy .text{margin-bottom:56px}
"""
    body = f"""<div class="wrap"><div class="ph">YOUR PHOTO</div>
<div class="copy"><h1>About</h1><div class="text">{BIO}</div>{CONTACT}</div></div>"""
    return page("A1", css, body, nav_on="About")


# ---------- A2: wide photo on top, bio and contact in two columns ----------
def about_2():
    css = ABOUT_CSS + """
.ph{height:62vh;margin:0 64px}
.cols{display:grid;grid-template-columns:2fr 1fr;gap:96px;padding:56px 64px 96px;max-width:1240px}
.cols h1{margin-bottom:24px}
"""
    body = f"""<div class="ph">YOUR PHOTO</div>
<div class="cols"><div><h1>About</h1><div class="text">{BIO}</div></div><div style="padding-top:12px">{CONTACT}</div></div>"""
    return page("A2", css, body, nav_on="About")


# ---------- A3: centered single column ----------
def about_3():
    css = ABOUT_CSS + """
.col{max-width:620px;margin:0 auto;padding:8px 24px 96px;text-align:center}
.ph{height:56vh;margin-bottom:48px}
.col h1{margin-bottom:24px}
.col .text{margin-bottom:48px}
.contact{align-items:center}
.contact a{align-self:center}
"""
    body = f"""<div class="col"><div class="ph">YOUR PHOTO</div><h1>About</h1><div class="text">{BIO}</div>{CONTACT}</div>"""
    return page("A3", css, body, nav_on="About")


PAGES = {
    "piece-1": piece_1, "piece-2": piece_2, "piece-3": piece_3, "piece-4": piece_4,
    "about-1": about_1, "about-2": about_2, "about-3": about_3,
}


def render(name):
    """Screenshot the whole page at 1440px wide, cropped to its content."""
    html, png = HERE / f"{name}.html", HERE / f"{name}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--virtual-time-budget=8000", "--window-size=1440,3000",
                    f"--screenshot={png}", f"file://{html.resolve()}"],
                   check=True, capture_output=True)
    im = Image.open(png).convert("RGB")
    box = ImageChops.difference(im, Image.new("RGB", im.size, "white")).getbbox()
    im.crop((0, 0, im.width, max(900, min(im.height, box[3] + 40)))).save(png)


if __name__ == "__main__":
    prepare_assets()
    for name, fn in PAGES.items():
        (HERE / f"{name}.html").write_text(fn())
        render(name)
        print("rendered", name)
