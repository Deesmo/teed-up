import os
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def download(url, path):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            with open(path, 'wb') as f:
                f.write(response.read())
        print(f"Saved {path} ({os.path.getsize(path) / 1024:.1f} KB)")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

assets_dir = "/Users/bradvaldesmacminipro/teedup-site/assets"

images = [
    ("hero.jpg", "xaawRgDfw3o", 1600),
    ("club-1.jpg", "lz0PyH5kRuE", 800),
    ("club-2.jpg", "pI6IaynZQ_I", 800),
    ("club-3.jpg", "RPizO9V8bIQ", 800),
    ("club-4.jpg", "OeftYAzu5jA", 800),
    ("club-5.jpg", "vQqumk0omac", 800),
    ("club-6.jpg", "xuQ-VFaCJyw", 800)
]

for name, id_, width in images:
    url = f"https://images.unsplash.com/photo-{id_}?w={width}&q=80&auto=format&fit=crop"
    download(url, os.path.join(assets_dir, name))
