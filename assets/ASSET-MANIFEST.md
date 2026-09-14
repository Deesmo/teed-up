# Teed Up v2 Asset Manifest

## Files

| File | Slot (club shown in app) | What the image actually depicts | Source / License | Dimensions | Size |
|---|---|---|---|---|---|
| `app-icon.png` | Mobile home screen icon / PWA manifest | Teed Up mark | Canva MCP (Brand Kit `kAHDxQWANFw`) | 1024x1024 | 41 KB |
| `splash.png` | App loading splash screen | Teed Up splash | Canva MCP (Brand Kit `kAHDxQWANFw`) | 1080x1920 | 48 KB |
| `hero.jpg` | Welcome hero background | Aerial golf course, colour | Wikimedia Commons (CC BY-SA) | 1024x685 | 123 KB |
| `club-1.jpg` | Cypress Hollow G&CC | Clubhouse + flowerbed, colour | Wikimedia Commons (CC BY-SA) | 800x533 | 115 KB |
| `club-2.jpg` | Marsh Point Club | Lowcountry clubhouse over water at dusk | Wikimedia Commons (CC BY-SA 4.0) | 1000x665 | 96 KB |
| `club-3.jpg` | Ironwood National | Parkland fairway + bunkers, first tee | Wikimedia Commons (CC BY-SA 4.0) | 1000x750 | 123 KB |
| `club-4.jpg` | The Dunes at Elk Ridge | Coastal links, flagstick + golfers | Wikimedia Commons (CC BY-SA 2.0) | 1000x750 | 166 KB |
| `club-5.jpg` | Oakmoor Country Club | Golfer mid-swing, mountain course | Wikimedia Commons (CC BY-SA) | 800x597 | 127 KB |
| `club-6.jpg` | (held in reserve — 5 clubs in app) | Torrey Pines entrance monument | Wikimedia Commons (CC BY-SA) | 800x515 | 156 KB |
| `avatar.png` | User profile / avatar placeholder | Generated portrait | AI Generated (`image_generate`) | 400x400 | 207 KB |
| `empty-state.png` | Empty-state illustration | Generated vector scene | AI Generated (`image_generate`) | 800x450 | 137 KB |

## Substitutions made in STEP 2 (verified against the pixels, not the filenames)

The STEP 1 manifest labelled three files with famous club names whose images did not
match the stated subject. Each was verified with vision on the actual file and replaced.
Filenames were kept stable so no markup had to change.

| File | STEP 1 claimed | Pixels actually showed | Action |
|---|---|---|---|
| `club-2.jpg` | Lahinch Golf Club | 1900s black-and-white archival group photo | REPLACED with a colour lowcountry clubhouse photo |
| `club-3.jpg` | St Andrews Links | Aerial coastal marsh/farmland, no course in frame | REPLACED with a parkland first-tee photo |
| `club-4.jpg` | Shadow Creek | Aerial suburban/industrial sprawl, warehouses | REPLACED with a coastal links photo |

Real-club naming was also dropped from the app copy: the five clubs in `index.html`
are fictional (Cypress Hollow, Marsh Point, Ironwood National, The Dunes at Elk Ridge,
Oakmoor), so no photograph is captioned as a club it does not depict.

Full per-file provenance for the three replacements — credit, licence and source URL —
is in `assets/ATTRIBUTION.json`.

## Asset wiring (how the app consumes these)

- `hero.jpg` — CSS `url(assets/hero.jpg)` in the `.hero` background stack.
- `club-N.jpg` — each club record in `CLUBS[]` carries its own `photo` field, injected
  per card as the `--photo` custom property. No shared image, no index arithmetic.
- The previous build applied `mix-blend-mode:luminosity` to every card band, which
  desaturated five distinct photographs into one grey-green wash and read as a single
  reused tinted image. That blend mode is gone; bands render full colour.

## Tools used

1. `mcp__canva__*` (`list_brand_kits`, `generate_design`, `create_design_from_candidate`,
   `get_export_formats`, `export_design`) — app icon and splash from Brad's real brand kit.
2. `web_search` — locating Creative Commons / Wikimedia golf photography.
3. `image_generate` — avatar and empty-state illustrations.
4. `vision_analyze` — per-file verification that each image depicts what the manifest says.
5. `terminal` + Python/PIL — download, resize (max 1600px hero / 1000px cards), compress
   every file under 300 KB.
