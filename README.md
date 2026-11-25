# Melanie Dickinson — portfolio site

A static site built with [Eleventy](https://www.11ty.dev/). The gallery is the home page; each piece has its own page.

## Run it locally

```bash
npm install
npm start        # http://localhost:8080, rebuilds as you edit
```

`npm run build` writes the finished site to `_site/`.

## Where things live

| What | Where |
| --- | --- |
| Each piece (photos, videos, text) | `src/work/<slug>/` |
| Piece text, title, year, order | `src/work/<slug>/index.md` |
| About page (text, photo, contact links) | `src/about/index.md` (put your photo in `src/about/`) |
| Section headings ("Play Sculptures") | `src/_data/site.json` |
| Styles / small scripts | `src/assets/style.css`, `src/assets/site.js` |
| Page templates | `src/_includes/` |

### A piece's `index.md`

```yaml
---
title: "Drip II"
year: 2024
materials: Basswood
dimensions: 20 × 15 × 6 cm
section: main        # main, or large for Play Sculptures
order: 14            # position in the gallery
cover: cover.jpg     # photo used in the gallery and at the top of the page
media:               # the rest of the page, in order (photos or .mp4 videos)
  - drip2-4.jpg
  - drip2-5.jpg
hidden: false        # true hides it from the site
---

Text about the piece, in Markdown.
```

Empty fields (`year:` etc.) show as a dash.

## Adding or updating photos

Either drop photos straight into the piece's folder and list them under `media:`, or keep using `../Media/Main Gallery` and run:

```bash
npm run import-media
```

That copies web-sized versions of each piece's cover (from `Main Gallery`) and extra photos/videos (from `Main Gallery/Subpages`, matched by filename) into `src/work/`. It never overwrites an existing `index.md`; it tells you about any new files so you can add them to `media:`. The list of pieces and filename prefixes is at the top of `scripts/import_media.py`.

## Publishing

`.github/workflows/deploy.yml` builds and publishes to GitHub Pages on every push to `master` (Pages source: "GitHub Actions"). `src/CNAME` sets the domain (www.melaniedickinson.com). Pages kept from the old site (`/games.html`, `/asp.html`, `/publications/`) live in `src/games/` and are copied to the site root as-is.

