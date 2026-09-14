import os
import urllib.request
from PIL import Image

def download_and_resize(url, path, max_width):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            with open(path, 'wb') as f:
                f.write(response.read())
        
        # Resize and compress
        img = Image.open(path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        ratio = max_width / img.width
        if ratio < 1:
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        img.save(path, 'JPEG', quality=85, optimize=True)
        print(f"Saved {path} ({os.path.getsize(path) / 1024:.1f} KB)")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

assets_dir = "/Users/bradvaldesmacminipro/teedup-site/assets"
os.makedirs(assets_dir, exist_ok=True)

images = [
    ("hero.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e6/Golf_course_at_the_Broadmoor.jpg", 1600),
    ("club-1.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/bb/Golf_Course_in_the_Scottish_Borders.jpg", 800),
    ("club-2.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/df/Pebble_Beach_Golf_Links_Hole_7.jpg", 800),
    ("club-3.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/a2/Augusta_National_Golf_Club_Hole_10.jpg", 800),
    ("club-4.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/cb/St_Andrews_Golf_Course.jpg", 800),
    ("club-5.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/91/Muirfield_Golf_Course.jpg", 800),
    ("club-6.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/4c/Golf_course.jpg", 800)
]

for name, url, width in images:
    download_and_resize(url, os.path.join(assets_dir, name), width)
