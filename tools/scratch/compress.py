import os
from PIL import Image

def process(path, max_width=800, is_jpg=True):
    img = Image.open(path)
    if img.mode != 'RGB' and is_jpg:
        img = img.convert('RGB')
    
    ratio = max_width / img.width
    if ratio < 1:
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
    
    if is_jpg:
        img.save(path, 'JPEG', quality=80, optimize=True)
    else:
        # Save as PNG with optimization
        img.save(path, 'PNG', optimize=True)
    print(f"Compressed {path} ({os.path.getsize(path)/1024:.1f} KB)")

assets_dir = "/Users/bradvaldesmacminipro/teedup-site/assets"
process(os.path.join(assets_dir, "avatar.png"), max_width=400, is_jpg=False)
process(os.path.join(assets_dir, "empty-state.png"), max_width=800, is_jpg=False)

