"""Copy photos/videos from ../Media/Main Gallery into the site's content folders.

    npm run import-media        (or: python3 scripts/import_media.py)

For each piece in PIECES below this creates src/work/<slug>/ containing
web-sized copies of its cover (from Main Gallery) and extra media (from
Main Gallery/Subpages, matched by filename prefix), plus an index.md.

Re-running is safe: images/videos are refreshed, but an existing index.md is
never overwritten (so your text, titles and ordering edits are kept). If a
piece already has an index.md, new media files are copied in and reported so
you can add them to its `media:` list by hand.
"""
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT.parent / "Media" / "Main Gallery"
SUB = MEDIA / "Subpages"
OUT = ROOT / "src" / "work"
MAX_PX = 2400  # long edge of stored masters; the build makes smaller sizes

# (slug, title, section, cover file stem in Main Gallery, [Subpages prefixes])
# Order here is the gallery order.
PIECES = [
    ("fingerprint-i", "Fingerprint I", "main", "fingerprint1", ["fingerprint1-"]),
    ("cloud-i", "Cloud I", "main", "drip1", ["drip1-"]),
    ("starfield", "Starfield", "main", "starfield", []),
    ("column", "Column", "main", "column", ["column-"]),
    ("fingerprint-iv", "Fingerprint IV", "main", "fingerpint4", []),
    ("a-study-of-eyes", "A Study of Eyes", "main", "astudyofeyes", ["eyes-"]),
    ("bomb", "Bomb", "main", "spikes", []),
    # Gallery-only card that links to fingerprint-iv (see its index.md).
    ("fingerprint-iv-panel", "Fingerprint IV", "main", "fingerprint4-2", []),
    ("fingerprint-iii", "Fingerprint III", "main", "fingerprint3", ["fingerprint3-"]),
    ("wave", "Wave", "main", "wave", []),
    ("spiderweb", "Spiderweb", "main", "spiderweb-3", ["spiderweb"]),
    ("reaching", "Reaching", "main", "fingers", ["fingers-"]),
    ("fingerprint-v", "Fingerprint V", "main", "fingerprint5", []),
    ("cloud-ii", "Cloud II", "main", "drip2-2", ["drip2"]),
    ("leap", "Leap", "main", "woodrabbit", ["woodrabbit-"]),
    ("root", "Root", "main", "carrot", []),
    ("crow", "Crow", "main", "crow", []),
    ("bone-spoon", "Bone Spoon", "main", "bonespoon", ["bonespoon-"]),
    ("footed-i", "Footed I", "main", "footed2-3", ["footed2."]),
    ("footed-ii", "Footed II", "main", "footed1-2", ["footed1."]),
    ("cully-turtle", "Cully Turtle", "large", "cullyturtle-repaint",
     ["cullyturtle-repaint", "cullytortoise-"]),
    ("cully-turtle-original-paint", "Cully Turtle (original paint)", "large",
     "cullyturtle-originalpaint", ["cullyturtle-originalpaint-"]),
    ("wyeast-turtle", "Wy'east Turtle", "large", "wyeastturtle", ["wyeastturtle-"]),
    ("cully-rabbit", "Cully Rabbit", "large", "cullyrabbit-5", ["cullyrabbit"]),
    ("bubbles", "Bubbles", "large", "bubbles", ["bubbles-"]),
]

IMAGE_EXT = {".jpg", ".jpeg", ".png"}
VIDEO_EXT = {".mp4", ".mov"}


def natural_key(name):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name.lower())]


def find(folder, stem):
    for ext in IMAGE_EXT:
        for p in (folder / f"{stem}{ext}", folder / f"{stem}{ext.upper()}"):
            if p.exists():
                return p
    return None


def digest(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def save_image(src, dest_dir, name=None):
    dest = dest_dir / f"{name or src.stem}.jpg"
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((MAX_PX, MAX_PX))
    im.save(dest, quality=85, optimize=True, progressive=True)
    return dest.name


def save_video(src, dest_dir):
    """Re-encode to a web-friendly H.264 MP4 (max 1080px) plus a poster frame."""
    dest = dest_dir / f"{src.stem}.mp4"
    poster = dest_dir / f"{src.stem}-poster.jpg"
    if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
        encode = subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
             "-vf", "scale='min(1080,iw)':-2", "-c:v", "libx264", "-crf", "26",
             "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
             "-c:a", "aac", "-b:a", "96k", str(dest)], capture_output=True)
        if encode.returncode != 0:
            # This ffmpeg build has no H.264 encoder: keep the original
            # streams, just move metadata to the front for faster playback.
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-c", "copy",
                 "-movflags", "+faststart", str(dest)], check=True)
            if dest.stat().st_size > 50_000_000:
                print(f"! {dest.name} is {dest.stat().st_size // 1_000_000} MB; "
                      "consider compressing it before publishing")
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.5", "-i", str(dest),
             "-frames:v", "1", "-q:v", "3", str(poster)], check=True)
    return dest.name


def main():
    if not MEDIA.exists():
        sys.exit(f"Media folder not found: {MEDIA}")
    used = set()
    for order, (slug, title, section, cover_stem, prefixes) in enumerate(PIECES, 1):
        # Covers normally come from Main Gallery, but may live in Subpages.
        cover = find(MEDIA, cover_stem) or find(SUB, cover_stem)
        if not cover:
            print(f"! {slug}: cover '{cover_stem}' not in Main Gallery, skipped")
            continue
        folder = OUT / slug
        folder.mkdir(parents=True, exist_ok=True)
        seen = {digest(cover)}
        media = [save_image(cover, folder, name="cover")]
        used.add(cover.name)

        extras = sorted(
            (p for p in SUB.iterdir() if p.is_file()
             and any(p.name.startswith(pre) for pre in prefixes)
             and p.suffix.lower() in IMAGE_EXT | VIDEO_EXT),
            key=lambda p: natural_key(p.name)) if SUB.exists() else []
        for p in extras:
            h = digest(p)
            used.add(p.name)
            if h in seen:  # same photo already included under another name
                continue
            seen.add(h)
            if p.suffix.lower() in VIDEO_EXT:
                media.append(save_video(p, folder))
            else:
                media.append(save_image(p, folder))

        md = folder / "index.md"
        if md.exists():
            listed = md.read_text()
            missing = [m for m in media if m not in listed]
            if missing:
                print(f"+ {slug}: new media not yet listed in index.md: {', '.join(missing)}")
            continue
        media_yaml = "\n".join(f"  - {m}" for m in media[1:]) or "  []"
        md.write_text(f"""---
title: "{title}"
year:
materials:
dimensions:
section: {section}
order: {order}
cover: {media[0]}
media:
{media_yaml}
---
""".replace("media:\n  []", "media: []"))
        print(f"✓ {slug}: {len(media)} file(s)")

    leftovers = [p.name for p in [*MEDIA.iterdir(), *(SUB.iterdir() if SUB.exists() else [])]
                 if p.is_file() and p.suffix.lower() in IMAGE_EXT | VIDEO_EXT and p.name not in used]
    if leftovers:
        print("Not assigned to any piece:", ", ".join(sorted(leftovers, key=natural_key)))


if __name__ == "__main__":
    main()
