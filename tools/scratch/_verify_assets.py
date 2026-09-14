from PIL import Image
import hashlib, os
d = 'assets'
for f in sorted(os.listdir(d)):
    p = os.path.join(d, f)
    if not f.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    try:
        im = Image.open(p)
        size = f"{im.size[0]}x{im.size[1]}"
        im2 = im.convert('RGB').resize((8, 8))
        px = list(im2.getdata())
        avg = tuple(sum(c[i] for c in px) // len(px) for i in range(3))
    except Exception as e:
        size, avg = 'ERR', str(e)
    h = hashlib.md5(open(p, 'rb').read()).hexdigest()[:10]
    print(f"{f:26} {size:12} md5={h} avgRGB={avg} bytes={os.path.getsize(p)}")
