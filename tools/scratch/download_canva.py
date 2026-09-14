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

canva_app_icon = "https://export-download.canva.com/YLKv0/DAHVMbYLKv0/-1/0-5903609093914271307.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20260913%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260913T195023Z&X-Amz-Expires=80961&X-Amz-Signature=94cb965dbef7ad80813eb7e3a20946b7108a78b4e01d3e4ad10c8161974f3167&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Mon%2C%2014%20Sep%202026%2018%3A19%3A44%20GMT"
canva_splash = "https://export-download.canva.com/CRBHw/DAHVMfCRBHw/-1/0-2127340807638206413.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20260914%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260914T035904Z&X-Amz-Expires=52288&X-Amz-Signature=64fda9af7c55e3e8eaca49002e7c8ff907228a928f98ca5db7c5ee718c4991af&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Mon%2C%2014%20Sep%202026%2018%3A30%3A32%20GMT"

download(canva_app_icon, os.path.join(assets_dir, "app-icon.png"))
download(canva_splash, os.path.join(assets_dir, "splash.png"))
