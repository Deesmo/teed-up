import subprocess
import os
from PIL import Image

urls = {
    "hero.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Golf_course_Golfplatz_Wittenbeck_Mecklenburg_Ostsee_Baltic_Sea_Germany.jpg",
    "club-1.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/b6/AugustaNationalMastersLogoFlowers.jpg",
    "club-2.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/b6/Fore%21_And_Fore_more%21_%286574865193%29.jpg",
    "club-3.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/d5/St_Andrews_Links_%26_Town_from_the_air.jpg",
    "club-4.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/bc/The_Exclusive_and_Well-Hidden_Shadow_Creek_Golf_Course%2C_Las_Vegas%2C_Nevada_on_Flight_Between_Las_Vegas%2C_Nevada_and_Baltimore%2C_Maryland_%287235096790%29.jpg",
    "club-5.jpg": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Golfer_swing.jpg",
    "club-6.jpg": "https://upload.wikimedia.org/wikipedia/commons/f/f3/Torrey_Pines_Golf_Course_plaque.jpg"
}

assets_dir = "/Users/bradvaldesmacminipro/teedup-site/assets"
os.makedirs(assets_dir, exist_ok=True)

for name, url in urls.items():
    path = os.path.join(assets_dir, name)
    # Download with curl
    subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", url, "-o", path])
    
    try:
        # Resize and compress
        img = Image.open(path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        max_width = 1600 if name == "hero.jpg" else 800
        ratio = max_width / img.width
        if ratio < 1:
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        img.save(path, 'JPEG', quality=85, optimize=True)
        print(f"Processed {name} ({os.path.getsize(path)/1024:.1f} KB)")
    except Exception as e:
        print(f"Failed to process {name}: {e}")

