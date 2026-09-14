# Teed Up — v3 Asset Manifest

All photography is **licensed Adobe Stock**, acquired through Brad's Adobe account.
The v2 build's Wikimedia Commons / geograph.org.uk images have been retired to
`assets/_v2-archive/` and are no longer referenced by the app.

| File | Adobe Stock ID | Source resolution | Delivered | Slot |
|---|---|---|---|---|
| hero-wide.jpg | 529690747 | 7952x5304 | 2400x1200 | Welcome hero (desktop) |
| hero-tall.jpg | 529690747 | 7952x5304 | 1200x1600 | Welcome hero (phone) |
| club-1.jpg | 347433847 | 5464x3640 | 1400x1050 | Kestrel Ridge |
| club-2.jpg | 252615642 | 5464x3640 | 1400x1050 | Blackwater Cay |
| club-3.jpg | 320371424 | 6998x4788 | 1400x1050 | Pinewild Hollow |
| club-4.jpg | 505586815 | 4032x3024 | 1400x1050 | Sable Dunes |
| club-5.jpg | 286877599 | 5464x3640 | 1400x1050 | Caledon Palms |
| club-6.jpg | 635384739 | 3840x2160 | 1400x1050 | Cape Mirren |
| club-7.jpg | 327094972 | 6132x3160 | 1400x1050 | Vermillion Wash |

Every delivered file is a LANCZOS resize + centre crop of the licensed original, lightly
graded (saturation 1.06, contrast 1.05), progressive JPEG, each under 420 KB.

## Selection method
Candidate thumbnails were downloaded and assembled into a contact sheet, then reviewed
visually before any image was chosen. This is a direct fix for the v2 failure, where three
images were selected by filename and depicted something other than their label.

## Typography
- Display: **Fraunces** — variable optical-size serif, club names and headings
- UI / body: **Archivo** — tabular numerals for tee times, yardages, ratings and fees

## Why v2 looked bare-bones
Hermes has no stock-photography credential of any kind — no Adobe, Getty, Shutterstock,
Unsplash or Pexels key across its 140 environment variables. Its studio agent could only
reach `web_search`, which led it to free Creative Commons photography. Separately, the only
image-generation backend enabled was `image_gen/xai`, the weakest one installed.
`image_gen/openrouter` (gpt-image-2, Krea 2, Qwen Image 3 Pro, MAI-Image-2.5) is now
enabled across the main config and all eight profiles.
