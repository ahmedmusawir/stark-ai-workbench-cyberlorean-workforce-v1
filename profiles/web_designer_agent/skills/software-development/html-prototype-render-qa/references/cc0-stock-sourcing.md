# Sourcing licensed stock photography for design prototypes (validated recipe)

When a brief allows "locally delivered" imagery and tools/rights permit sourced photos,
the reliable zero-key path is the **Wikimedia Commons API**, not Unsplash/Pexels directly.
Direct Unsplash/Pexels page extraction returned no usable machine-readable license path in
tested runs (dynamic pages, no API key); Commons gives explicit per-file license metadata
over plain `urllib`.

## Working recipe (stdlib + Pillow)

```python
import urllib.request, urllib.parse, json, io
from PIL import Image
H = {'User-Agent': 'DesignStudy/1.0 (prototype research)'}  # UA is required; anonymous UAs get throttled

# 1) SEARCH — generator=search over File: namespace (gsrnamespace=6)
q = {'action':'query','generator':'search','gsrsearch':'typing laptop (Unsplash)',
     'gsrnamespace':'6','gsrlimit':'30','prop':'imageinfo',
     'iiprop':'url|extmetadata','iiurlwidth':'1200','format':'json'}
r = json.load(urllib.request.urlopen(urllib.request.Request(
    'https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(q), headers=H), timeout=30))

# 2) FILTER — keep only explicit CC0 image files
for page in r.get('query',{}).get('pages',{}).values():
    info = page['imageinfo'][0]; meta = info.get('extmetadata',{})
    if meta.get('LicenseShortName',{}).get('value') == 'CC0' \
       and page['title'].lower().endswith(('.jpg','.png')):
        print(page['title'], meta.get('Artist',{}).get('value',''))

# 3) FETCH one by exact title — use thumburl (resized), not the original multi-MB file
q = {'action':'query','titles':'File:Typing on a mac (Unsplash).jpg','prop':'imageinfo',
     'iiprop':'url|extmetadata','iiurlwidth':'1600','format':'json'}
info = next(iter(json.load(urllib.request.urlopen(urllib.request.Request(
    'https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(q), headers=H),
    timeout=30))['query']['pages'].values()))['imageinfo'][0]
assert info['extmetadata']['LicenseShortName']['value'] == 'CC0'   # hard-gate the license
data = urllib.request.urlopen(urllib.request.Request(info['thumburl'], headers=H), timeout=45).read()
Image.open(io.BytesIO(data)).convert('RGB').save('assets/photo.webp', quality=87, method=5)
```

## Query tips

- Generic subject searches ("laptop coding workspace") drown in PDF/document hits from
  institutional archives. Appending **`(Unsplash)`** to the query surfaces the large
  CC0 Unsplash-mirror collection on Commons — titled `File:<subject> (Unsplash).jpg`.
- Exclude `.pdf` results explicitly; `gsrnamespace=6` alone is not enough.
- Useful proven searches: `notebook (Unsplash)`, `writing (Unsplash)`,
  `typing laptop (Unsplash)`, `pen notebook Unsplash`.

## Provenance record (ASSET_PROVENANCE.json)

Record per image: local filename, Commons `File:` title, `descriptionurl` (source page),
`url` (original), `thumburl` (what was actually downloaded), `Artist` metadata HTML,
`LicenseShortName` + `LicenseUrl`, and a plain-language transformations line
("Commons 1920px thumbnail, crop (x1,y1,x2,y2), converted to WebP, CSS cover-crop").
State honestly that Commons metadata is the license basis, **not** an independent
chain-of-title audit.

## Mandatory inspection gate — license ≠ suitability

View every candidate with the vision tool BEFORE authoring HTML around it, and zoom into
legible details, not just the overall subject:

- **Inappropriate screen text.** A CC0 "laptop coding" photo was rejected in a real run
  because the visible code/editor content was unsuitable. The license was fine; the pixels
  were not. Document the rejection and the replacement in IMAGERY_PLAN.md.
- **Incidental third-party marks** (device logos, app chrome, brand stickers): crop them
  out in the Pillow step and record the crop box; if they can't be removed, drop the image.
- Dark/unreadable screens are safe; readable screens need word-by-word review.

Then restate in customer-facing-adjacent docs: contextual stock, never presented as the
client's staff, premises, portfolio, or results — and replaceable with authentic client
imagery in a later approved phase.
