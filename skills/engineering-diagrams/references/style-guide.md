# Style Guide

House style for hand-written SVG engineering diagrams. Start every new diagram from `assets/skeleton.svg`.

## Canvas and header

| Item | Rule |
|---|---|
| Size | Width 760-1240. Height fits the content. `viewBox`, `width`, `height` and the background rect always match. |
| Background | First drawable: full-size opaque rect `#fafaf9`. Never transparent, so it reads on GitHub dark pages. |
| Margin | 40px on every side. The legend strip sits inside the bottom margin area. |
| Grid | Snap coordinates to 4px. Box widths in steps of 20. |
| Eyebrow | `x=40 y=32`, 10px uppercase mono, letter-spacing `.14em`, `#64748b`: `TYPE · WORK-ID · PLAN 3, 4` (or `SPEC AC-2`, or `STANDALONE`). |
| Title | `y=62`, 28px serif `'Instrument Serif', 'Iowan Old Style', Georgia, serif`, `#0f172a`. 2-6 words; no feature prefix (the eyebrow carries it). |
| Subtitle | `y=84`, 13px sans `#475569`. One sentence stating the claim the diagram makes. |
| Content | Starts at `y >= 110`. |

## Color roles

Use at most five roles per diagram. Never let color carry meaning alone: pair it with a tag, line style, shape or legend text.

| Role | Fill | Stroke | Text on fill | Use |
|---|---|---|---|---|
| Existing | `#ffffff` | `#64748b` | `#0f172a` / `#475569` | Code, tables, services that exist today |
| New | `#f0fdfa` | `#0f766e` | `#0f172a` / `#475569` | Introduced by this work |
| New, focal | `#ccfbf1` | `#0f766e` | `#0f172a` / `#475569` | The 1-2 elements the diagram is about |
| Decision or note | `#fffbeb` | `#d97706` | `#92400e` for emphasis | Branch questions, rules, caveats |
| Failure or deletion | `#fef2f2` | `#b91c1c` | `#b91c1c` | Errors, rejections, removals |
| External | `#fff7ed` | `#c2410c` | `#9a3412` | Third parties, storage, mail providers |

Lines: neutral `#475569`, secondary/dashed `#64748b`, new path `#0f766e`, failure `#b91c1c`, hairline `#e7e5e4`. Text: ink `#0f172a`, soft `#475569`, legend `#334155`.

Measured contrast: `#475569` on paper 7.3:1, `#64748b` on paper 4.6:1 (eyebrow and secondary lines only), `#0f766e` on `#f0fdfa` 5.3:1, `#b91c1c` on `#fef2f2` 5.9:1, `#92400e` on `#fffbeb` 6.8:1. `#d97706` is 3.1:1, so use it for strokes only, never for text.

## Typography

| Element | Size | Weight | Family |
|---|---|---|---|
| Node name | 15 | 600 | sans |
| Sublabel | 12 | 400 | sans, `#475569` |
| Code identifier (table, method, column, route) | 11-12 | 400 | mono `ui-monospace, SFMono-Regular, Menlo, monospace` |
| Edge label | 12 | 400 | sans, sentence case; code parts in 11px mono |
| Tag | 9 | 700 | sans uppercase, letter-spacing `.06em` |
| Section heading inside a diagram | 11 | 700 | sans uppercase, letter-spacing `.08em`, `#475569` |
| Legend | 12 | 400 | sans `#334155` |

Sans stack: `Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif` (set on the root `<svg>`). Do not embed or link fonts. Minimum size is 9px for uppercase tags and 11px for anything else.

## Shapes

| Element | Rule |
|---|---|
| Node | `rx=6`, stroke 1.5. Two text lines: height 64, name baseline +28, sublabel +48, left padding 16. |
| Container, frame, swimlane | `rx=8`, stroke 1, set `data-role="frame"` so line-crossing checks ignore it. |
| Note | Note color role, `rx=6`, `data-role="note"` when it sits on a lifeline. |
| Tag | `rx=2` rect, 16 high, white fill, stroke = role color, text = role color. Top-right corner, 8px inset. Tags: `NEW`, `EXISTING`, `EXTERNAL`, `CHANGED`, `FINAL`, `ASYNC`. |
| Decision | Note color role. A diamond for small flows; a rounded box phrased as a question when text is long. Either way every exit is labeled. |
| Storage | Cylinder only for blob or object storage; tables use ERD boxes. Mark its unfilled top arc `data-role="shape"` so it is not treated as a connector. |
| Start / end | Filled dot r=6 / ring r=8 around a dot r=4.5. |

## Connectors

1. Route orthogonally. Round each elbow with `Q` at radius 8. A straight segment only when both ends share an axis.
2. Leave and enter boxes perpendicular to the edge, at least 12px from a corner.
3. Stop the path 2px short of the target edge so the arrowhead touches it.
4. Several edges on one side: spread attach points at `side * k / (n + 1)`, at least 12px apart.
5. Keep parallel runs 24px apart (12px minimum). Never stack two strokes on one line.
6. Never pass through or behind a box that is not an endpoint. Move boxes or reserve a corridor instead.
7. Avoid crossings. When one is unavoidable, add a hop: a 5px semicircle on the later-drawn line.
8. One stroke width (1.5) for all connectors. Solid = call or link; dashed `5 4` = return, reverse or optional; open arrowhead (`slug-arr-open`) = async or fire-and-forget.
9. Label every edge unless the legend makes the meaning obvious (for example sequence returns). Labels: 12px, at most about 30 characters, wrapped onto 2 lines before growing longer.
10. Put labels beside vertical segments, never across them. On horizontal segments, sit the label on a mask rect filled with the background color, 16px tall, 4px wider than the text on each side.
11. Paint order: background, header, frames, connectors, label masks and labels, nodes, tags, legend.

## Legend and notes

- Wrap the legend in `<g id="legend">` under a hairline at the bottom. List only the symbols actually used: each fill role, each tag, each line style and arrowhead.
- Global transitions ("any state can be deleted") become one `* -> X` line above the legend instead of many edges.
- Footnotes go above the legend in 12px `#475569`. Keep at most two.

## SVG hygiene

- Root: `role="img"` and `aria-labelledby="<slug>-title <slug>-desc"`. `<title>` is the first child (80 characters max) and `<desc>` follows with one or two sentences about meaning.
- Prefix every id with the diagram slug (`lifecycle-arr`, `lifecycle-title`) so several diagrams can be inlined into one page.
- Escape `<`, `>` and `&` as `&lt;`, `&gt;` and `&amp;`.
- No `<script>`, `<foreignObject>`, `<image>`, external `href`, `@import` or event attributes.
- Prefer presentation attributes over `<style>` classes; the checker understands only simple class selectors.
- When rows are added, update the `viewBox`, `width`, `height` and background rect together, then move the legend down.

## Limitations

- Light only. GitHub dark pages show the diagram as a light card, which is acceptable. `prefers-color-scheme` inside SVG follows the OS, not GitHub's theme toggle, so it is not used.
- Fonts fall back by platform. Leave 12px or more of padding so wider fallback fonts still fit.
