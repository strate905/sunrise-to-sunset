# Bundled Font Guidance

Place cross-language fonts in this directory so the chart renderer can load them automatically.

Recommended pairings:
- IBM Plex Sans (Latin coverage)
- IBM Plex Sans Arabic
- Noto Sans CJK JP (covers Japanese full-width glyphs)

Matplotlib automatically registers any `.ttf` or `.otf` files found here when you run the CLI, so you do not need to tweak system font paths. Without these fonts installed, the application falls back to whatever fonts are already on your machine, which may miss some glyphs.
