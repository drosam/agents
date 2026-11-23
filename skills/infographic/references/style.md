# Style

One look for both renderers: clean flat infographic, soft pastels, rounded cards, thin outlines, simple line icons, generous spacing. The brief describes it in words; the SVG uses these tokens.

## Canvas

- 16:9, `viewBox="0 0 1600 900"`, `width="1600" height="900"`.
- Margins 60px left and right; title baseline about y=70; footer baseline about y=870.
- Opaque background rect: `#F8FAFC`. Before / after halves: left `#F7F4EF` (warm), right `#F1F5F9` (cool).

## Color meaning

| Role | Stroke / text | Fill |
|---|---|---|
| Text, titles | `#0F172A` | - |
| Descriptions | `#475569`; small notes `#64748B` | - |
| Entry points, actors, primary objects | `#3B82F6`, `#2563EB`, text `#1E3A8A` | `#DBEAFE`, `#EFF6FF` |
| Data, storage, internals | `#14B8A6`, text `#0F766E` / `#134E4A` | `#CCFBF1` |
| Fixed, success, after | `#16A34A`, text `#166534` | `#DCFCE7` |
| Guardrails, rules, caution | `#F59E0B`, icon `#B45309` | `#FEF3C7` |
| Problem, before, deleted | `#DC2626`, text `#991B1B` | `#FEE2E2` |
| Neutral objects | `#94A3B8`, `#CBD5E1` | `#FFFFFF`, `#E2E8F0` |

Color never carries meaning alone: pair it with a word, icon, check or X.

## Type

Font stack `Inter, "Helvetica Neue", Arial, sans-serif`; mono `"JetBrains Mono", Menlo, Consolas, monospace` for file names, code, API paths.

| Use | Size / weight |
|---|---|
| Title | 40-44 bold |
| Half heading ("BEFORE ...") | 32: keyword 800, claim 400 |
| Section header | 19 bold uppercase, letter-spacing 1.5 |
| Card title | 22 semibold (slim rows 18) |
| Body, bullets | 16-17 |
| Notes, sub-lines, chips | 14-15; never below 13 |
| Caption under a half | 21 bold, dark red or dark green |

Width estimate: about 0.55 x size per character for sans, 0.6 x size for mono. Keep 16px padding inside cards.

## Shapes and icons

- Cards: `rx` 12-14, white fill, 1.5px role stroke, soft shadow filter from the skeleton.
- Pills and chips: `rx` = half the height.
- Arrows: 2-2.2px, marker from the skeleton; curves are fine for fan-out and flows.
- Icons: inline paths, 2-2.2px stroke, round joins, role color. Common set: document with folded corner, envelope, clock, flag, upload arrow, check circle, X circle, question badge, browser window with three dots, database cylinder, server stack, person (head circle + shoulders arc), paperclip, repeat arrow, calendar row.
- Mock UI (history rows, tables, dialogs) uses gray placeholder bars for text that does not matter.

## SVG rules

- `role="img"`, `<title>` first child, `<desc>` with a one or two sentence summary, `aria-labelledby` pointing at both.
- Self-contained: no `<image>`, `<script>`, `<foreignObject>`, external `href` or web fonts.
- Repeated shapes go in `<defs>` and are placed with `<use href="#id">`.
- Runs of spaces collapse in SVG text. Separate parts with ` · ` or use separate `<text>` / `<tspan x=...>` elements.
- Use straight quotes and ASCII in markup; `·` and real product names are fine in visible text.

## Preview for the visual check

The preview is only for looking; write it to the temp dir and never deliver it. From this skill's directory, the sibling `engineering-diagrams` skill has a renderer:

```bash
python3 ../engineering-diagrams/scripts/render_png.py <file.svg> /tmp/infographic/<name>.png --scale 1
```

Without it, any Chromium-family browser works:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1600,900 --screenshot=/tmp/infographic/<name>.png file://<absolute-path>.svg
```

No browser: report "visual check skipped".
