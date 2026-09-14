#!/usr/bin/env python3
"""Search Wikimedia Commons for freely-licensed golf course photography.
Reports candidates with license + dimensions so a human/agent can pick deliberately.
"""
import json
import sys
import urllib.parse
import urllib.request

UA = "TeedUpAssetSourcing/1.0 (local prototype; contact brad@example.com)"
API = "https://commons.wikimedia.org/w/api.php"


def api(params):
    params = dict(params, format="json")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def search(term, limit=14):
    d = api({
        "action": "query", "generator": "search",
        "gsrsearch": f"filetype:bitmap {term}",
        "gsrnamespace": 6, "gsrlimit": limit,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata",
        "iiurlwidth": 1200,
    })
    out = []
    for page in (d.get("query", {}).get("pages") or {}).values():
        ii = (page.get("imageinfo") or [{}])[0]
        if not ii:
            continue
        meta = ii.get("extmetadata", {})
        lic = meta.get("LicenseShortName", {}).get("value", "?")
        w, h = ii.get("width", 0), ii.get("height", 0)
        if w < 900 or h < 500:
            continue
        if w / max(h, 1) < 1.2:          # want landscape for card bands
            continue
        out.append({
            "title": page["title"],
            "license": lic,
            "artist": _strip(meta.get("Artist", {}).get("value", "")),
            "dims": f"{w}x{h}",
            "thumb": ii.get("thumburl"),
            "src": ii.get("url"),
        })
    return out


def _strip(html):
    import re
    return re.sub(r"<[^>]+>", "", html).strip()[:70]


if __name__ == "__main__":
    terms = sys.argv[1:] or ["golf course fairway green"]
    allc = {}
    for t in terms:
        for c in search(t):
            allc[c["title"]] = c
    ok = [c for c in allc.values()
          if any(k in c["license"].lower() for k in ("cc", "public domain", "cc0"))]
    print(json.dumps(ok, indent=1))
    print(f"\n{len(ok)} freely-licensed landscape candidates", file=sys.stderr)
