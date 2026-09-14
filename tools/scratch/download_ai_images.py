import os
import urllib.request

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

download("https://v3b.fal.media/files/b/0aaa6adf/jOHg-LiepzIzDSMC0mF4N_G0QxyhcW.png", os.path.join(assets_dir, "avatar.png"))
download("https://v3b.fal.media/files/b/0aaa6adf/2wxXoEyLiaki87g63p9r9_ql8DZnBQ.png", os.path.join(assets_dir, "empty-state.png"))
