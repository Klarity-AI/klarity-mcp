# assets/

Brand assets for Within MCP.

## Current state

The live product surfaces reference only the docs-site assets, which are
committed under `docs/`:

- `docs/logo/within-logo-light.png` — docs header logo (light mode), 512×512
- `docs/logo/within-logo-dark.png` — docs header logo (dark mode), 512×512
- `docs/favicon.png` — browser-tab icon, 192×192

These are the Within icon (orange rounded square with the white "W" mark).

## Masters

The icon and wordmark exist as vector masters and are the source of truth for
any raster export:

- Within icon (square mark) — SVG
- Within wordmark (mark + "Within" name) — SVG

Export PNGs from these when a new size is needed. Standard icon sizes:
1092, 512, 216, 192, 90, 48 (plus a 32×32 white-on-transparent outline variant
for the Microsoft 365 app-package, which is NOT a plain recolor of the icon).

## Store-listing assets (not yet added)

Vendor app-store listings (OpenAI / Anthropic / Microsoft 365) additionally
require a hero/banner image and product screenshots. These are prepared at
submission time and are not committed here yet.
