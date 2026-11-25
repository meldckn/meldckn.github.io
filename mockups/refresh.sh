#!/bin/sh
# Re-sync mockup images from Media/Main Gallery, regenerate HTML and render variant B.
# Usage (from repo root):  sh mockups/refresh.sh
set -e
cd "$(dirname "$0")"
rm -f assets/*.jpg
python3 - <<'PY'
from PIL import Image, ImageOps
import os, glob
src = '../../Media/Main Gallery'
for p in sorted(glob.glob(src + '/*.jpg') + glob.glob(src + '/*.png')):
    im = ImageOps.exif_transpose(Image.open(p)).convert('RGB')
    im.thumbnail((1000, 1000))
    im.save('assets/' + os.path.splitext(os.path.basename(p))[0] + '.jpg', quality=85)
PY
python3 generate.py > /dev/null
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --hide-scrollbars --virtual-time-budget=10000 --window-size=1440,10000 \
  --screenshot="$PWD/variant-b.png" "file://$PWD/variant-b.html" 2>/dev/null
python3 - <<'PY'
from PIL import Image, ImageChops
im = Image.open('variant-b.png').convert('RGB')
bbox = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).getbbox()
im.crop((0, 0, im.width, bbox[3] + 80)).save('variant-b.png')
PY
python3 -c "
import generate as g
for label, ps in g.SECTIONS: print(label or 'Main', [t for t, y, s in ps])"
