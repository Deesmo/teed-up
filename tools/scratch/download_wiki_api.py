import os
import urllib.request
import json
from PIL import Image

def download_and_resize(url, path, max_width):
    req = urllib.request.Request(url, headers={'User-Agent': 'TeedUpBot/1.0'})
    try:
        with urllib.request.urlopen(req) as response:
            with open(path, 'wb') as f:
                f.write(response.read())
        
        img = Image.open(path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        ratio = max_width / img.width
        if ratio < 1:
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        img.save(path, 'JPEG', quality=85, optimize=True)
        print(f"Saved {path} ({os.path.getsize(path) / 1024:.1f} KB)")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

# Get images from Wikipedia API
search_url = "https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&generator=search&gsrsearch=golf%20course&gsrnamespace=0&gsrlimit=10&piprop=original&format=json"

req = urllib.request.Request(search_url, headers={'User-Agent': 'TeedUpBot/1.0'})
response = urllib.request.urlopen(req)
data = json.loads(response.read())

pages = data['query']['pages']
urls = []
for page_id in pages:
    if 'original' in pages[page_id]:
        urls.append(pages[page_id]['original']['source'])

print(f"Found {len(urls)} images")

assets_dir = "/Users/bradvaldesmacminipro/teedup-site/assets"
os.makedirs(assets_dir, exist_ok=True)

names = [
    ("hero.jpg", 1600),
    ("club-1.jpg", 800),
    ("club-2.jpg", 800),
    ("club-3.jpg", 800),
    ("club-4.jpg", 800),
    ("club-5.jpg", 800),
    ("club-6.jpg", 800)
]

count = 0
for i, url in enumerate(urls):
    if count >= len(names):
        break
    # Skip non-jpgs to be safe
    if not url.lower().endswith(('.jpg', '.jpeg')):
        continue
    
    name, width = names[count]
    if download_and_resize(url, os.path.join(assets_dir, name), width):
        count += 1
