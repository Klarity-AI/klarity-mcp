# assets/

Marketing and submission assets for Within MCP across vendor app stores.

## Layout

```
assets/
  logos/         # square brand logo at multiple sizes (master + downscaled)
  hero/          # hero/banner image for store listings
  screenshots/   # product screenshots (vendor-neutral filenames)
  app-package/   # Microsoft 365 app-package icons (filenames pinned to manifest)
```

## Naming convention

`within-{kind}-{WIDTH}x{HEIGHT}.{ext}` — sortable, self-describing, vendor-neutral.

Exception: `app-package/color.png` and `app-package/outline.png` use Microsoft's
required filenames so they match the `icons` block in `manifest.json`.

## Vendor mapping

**Microsoft 365 Copilot — Partner Center listing**
- `logos/within-logo-48x48.png` (small)
- `logos/within-logo-90x90.png` (medium)
- `logos/within-logo-216x216.png` (large)
- `hero/within-hero-815x378.png`
- `screenshots/within-screenshot-1-1366x768.png`
- `screenshots/within-screenshot-2-1366x768.png`

**Microsoft 365 Copilot — app-package zip** (filenames must match `manifest.json`)
- `app-package/color.png` (192x192, full color)
- `app-package/outline.png` (32x32, transparent + white only, dedicated K-mark)

**OpenAI / Anthropic / general listings**
- `logos/within-logo-512x512.png`
- `screenshots/within-screenshot-{1,2}-original.png` (706x557, 706x478)

## Sources

- Master logo (1092x1092): `~/Downloads/within-logo-1092x1092.png`, identical
  (sha256-matched) to `within-mcp/logo.png` at the repo root.
- Outline source (white K on transparent): `~/Downloads/K-White.png` (243x292).
  Distinct from the full-color logo — used only for `app-package/outline.png`.
  Cleaned + archived at `logos/within-logo-mark-white-243x292.png`.
- Hero source: `~/Downloads/withinai_cover.jpeg` (1128x191 banner).
  Letterboxed onto extended-edge gradient to fit 815x378.
- Screenshot sources: `~/Desktop/within-chatgpt-app-screenshot-{1,2}.png`.
  Renamed to vendor-neutral `within-screenshot-{1,2}-*` and letterboxed onto
  the matching dark-gray background (#212121) to fit 1366x768.

## Regeneration

All assets derive from the master `logo.png` plus the source files above.
To regenerate logos at new sizes (requires Pillow in the active env):

```bash
poetry run python3 - <<'PY'
from PIL import Image
master = Image.open("logo.png")
for s in (1092, 512, 216, 192, 90, 48):
    out = f"assets/logos/within-logo-{s}x{s}.png"
    img = master if s == 1092 else master.resize((s, s), Image.LANCZOS)
    img.save(out, "PNG", optimize=True)
PY
```

The Microsoft `app-package/outline.png` is not derived from `logo.png`; see
the recipe in the original asset-generation task — it uses the dedicated
white-on-transparent K mark and force-whitens any non-transparent pixels.
