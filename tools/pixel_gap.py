#!/usr/bin/env python3
"""Deterministic overlap check: no vision opinion, just pixels.

For each v4 screenshot, scan upward from the bottom to locate:
  - the nav bar's top border (the 1px light line above the opaque nav background)
  - the lowest non-background content pixel ABOVE that border

If content's lowest row is above the nav border, nothing is covered. We also
assert the nav strip itself is opaque (uniform dark), which is what "content
bleeds through behind it" would violate.
"""
import sys
from PIL import Image

SHOTS = "/Users/bradvaldesmacminipro/hermes-workspace/teed-off/shots-v4"
DSR = 2
NAV_H_CSS = 64
BG = (10, 14, 12)          # --bg
BODY_BG = (5, 16, 11)      # body background


def close(px, ref, tol=6):
    return all(abs(a - b) <= tol for a, b in zip(px[:3], ref))


def analyse(name):
    im = Image.open(f"{SHOTS}/{name}.png").convert("RGB")
    W, H = im.size
    nav_top_px = H - NAV_H_CSS * DSR          # expected nav top row
    px = im.load()

    # 1. Is the nav strip opaque and uniform? Sample a grid inside the nav,
    #    skipping the label text rows by taking only rows near its edges.
    nav_rows = [nav_top_px + 4, nav_top_px + 10, H - 8, H - 4]
    impurities = 0
    for y in nav_rows:
        for x in range(0, W, 7):
            if not close(px[x, y], BG, tol=10):
                impurities += 1
    total = len(nav_rows) * len(range(0, W, 7))

    # 2. Lowest content pixel strictly ABOVE the nav top border.
    lowest_content = None
    for y in range(nav_top_px - 1, -1, -1):
        row_has_content = False
        for x in range(0, W, 3):
            p = px[x, y]
            if not (close(p, BG, 10) or close(p, BODY_BG, 10)):
                row_has_content = True
                break
        if row_has_content:
            lowest_content = y
            break

    gap_css = (nav_top_px - lowest_content) / DSR if lowest_content else None
    return {
        "screen": name,
        "size": f"{W}x{H}",
        "css_size": f"{W//DSR}x{H//DSR}",
        "nav_top_px": nav_top_px,
        "nav_opaque": f"{total - impurities}/{total} sampled nav px are exact --bg",
        "lowest_content_px": lowest_content,
        "gap_css_px": gap_css,
        "verdict": "CLEAR" if gap_css and gap_css > 0 else "OVERLAP",
    }


if __name__ == "__main__":
    screens = ["discover", "club-detail", "host", "profile"]
    bad = 0
    for s in screens:
        r = analyse(s)
        print(f"{r['screen']:<12} {r['css_size']:>9}  navTop={r['nav_top_px']:>4}px  "
              f"lowestContent={r['lowest_content_px']:>4}px  gap={r['gap_css_px']:>5}css  "
              f"{r['verdict']}   nav opaque: {r['nav_opaque']}")
        if r["verdict"] != "CLEAR":
            bad += 1
    # welcome has no nav at all
    im = Image.open(f"{SHOTS}/welcome.png").convert("RGB")
    print(f"welcome      {im.size[0]//DSR}x{im.size[1]//DSR}  (no nav bar on welcome by design)")
    print("\nRESULT:", "ALL CLEAR" if bad == 0 else f"{bad} SCREEN(S) OVERLAP")
    sys.exit(1 if bad else 0)
