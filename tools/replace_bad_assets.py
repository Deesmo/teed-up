#!/usr/bin/env python3
"""Replace the three mislabeled club photos with real, freely-licensed golf
course photography. Writes ATTRIBUTION rows to stdout for the manifest.

Only club-2/3/4 are replaced; club-1, club-5, club-6 and hero.jpg were verified
by eye as genuine golf photography and are left untouched.
"""
import io
import json
import os
import time
import urllib.error
import urllib.request

from PIL import Image

UA = "TeedUpAssetSourcing/1.0 (local prototype)"
OUT = "assets"
MAX_W = 1000
TARGET_KB = 260

# (filename, commons source URL, credit, license, why this club)
PICKS = [
    ("club-2.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/c/ce/Coastal_Links_Shell_Point.jpg",
     "Sswebrc / Wikimedia Commons", "CC BY-SA 4.0",
     "Marsh Point Club - Charleston lowcountry coastal links"),
    ("club-3.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/4/41/Kingsley_Club_-_First_Tee.jpg",
     "Ben Scripps / Wikimedia Commons", "CC BY-SA 4.0",
     "Ironwood National - championship parkland first tee"),
    ("club-4.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/f/fa/Balcomie_Links_from_the_Fife_Coastal_Path_-_geograph.org.uk_-_4107488.jpg",
     "Sandy Gemmill / Wikimedia Commons", "CC BY-SA 2.0",
     "The Dunes at Elk Ridge - clifftop ocean links"),
]


def fetch(url):
    """Commons rate-limits bursts with 429; back off and retry rather than fail."""
    import random
    import time
    last = None
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            last = e
            if e.code not in (429, 503):
                raise
            wait = min(60, 5 * 2 ** attempt) + random.uniform(0, 3)
            print(f"  {e.code} on attempt {attempt+1}; sleeping {wait:.1f}s")
            time.sleep(wait)
    raise last


def save(img, path):
    """Shrink to MAX_W then step quality down until under TARGET_KB."""
    if img.width > MAX_W:
        img = img.resize((MAX_W, round(img.height * MAX_W / img.width)), Image.LANCZOS)
    img = img.convert("RGB")
    for q in (86, 80, 74, 68, 62, 56):
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() <= TARGET_KB * 1024:
            break
    with open(path, "wb") as f:
        f.write(buf.getvalue())
    return img.size, buf.tell(), q


rows = []
for name, url, credit, lic, why in PICKS:
    raw = fetch(url)
    dims, size, q = save(Image.open(io.BytesIO(raw)), os.path.join(OUT, name))
    rows.append({"file": name, "dims": f"{dims[0]}x{dims[1]}", "bytes": size,
                 "quality": q, "credit": credit, "license": lic, "slot": why,
                 "source": url})
    print(f"{name}: {dims[0]}x{dims[1]} {size//1024}KB q{q}  <- {credit} ({lic})")
    time.sleep(4)  # be polite to Commons between downloads

with open("assets/ATTRIBUTION.json", "w") as f:
    json.dump(rows, f, indent=1)
print("\nwrote assets/ATTRIBUTION.json")
