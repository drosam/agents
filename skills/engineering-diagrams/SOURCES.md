# Engineering Diagrams Sources

Created: 2026-11-23. Class: workflow-process (artifact generator). Shape: script-backed workflow with routed references and one template asset.

Trigger: the user reviewed hand-written SVGs in a private work item, asked for best practices, nicer styling and existing skills to reuse, then chose to build a local skill that keeps hand-written SVG, grounds diagrams in the spec and plan, and uses a hybrid style. The user required checking licenses of every skill and resource used.

## License policy

Local synthesis. No upstream text, code, scripts or assets were copied. Ideas were restated in our own words, and every source was checked for a license before use. Sources without a license file were used for ideas only. This repository is MIT; MIT, Apache-2.0, ISC and CC BY sources are compatible with that use.

## Pattern references (agent skills)

| Source | Revision inspected | License (verified) | Used for | Not taken |
|---|---|---|---|---|
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | `0eeda75a708f419560d5e032693618bb9954f17b` | MIT, LICENSE file, (c) 2025 Cathryn Lavery | Ideas: orthogonal elbows, attach-point spreading, masked labels, paint order, type tags, density budgets, a11y contract, render-and-name-a-defect loop, ERD key prefixes, sequence arrow grammar, lifecycle bands | Text, palette values, fonts, icons, scripts, HTML output |
| [yizhiyanhua-ai/fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph) | `1ca1ff9cfcb67893a43d32b9ef3a1b782c44a46f` | MIT, LICENSE file, (c) 2025 fireworks-tech-graph contributors | Ideas: "successful command is not a visual verdict", change approach after two unchanged failures, route budgets | Styles, scripts, data-graph tagging |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | default branch, 2026-11-23 | Apache-2.0 (GitHub API) | Idea: validate before declaring done | Everything else |
| [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) `mermaid-diagrams` | default branch, 2026-11-23 | MIT (GitHub API) | Idea: type selection by reader question | Mermaid syntax |
| [diegomarino/claude-toolshed](https://github.com/diegomarino/claude-toolshed) `d2` | default branch, 2026-11-23 | ISC declared in package.json; no LICENSE file | Ideas only: one abstraction level, one grouping criterion | Any text |
| [spillwavesolutions/design-doc-mermaid](https://github.com/spillwavesolutions/design-doc-mermaid) | default branch, 2026-11-23 | README claims MIT; no LICENSE file | Ideas only: never embed an unvalidated diagram | Any text |
| [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) | default branch, 2026-11-23 | None found | Ideas only: diagrams argue rather than display | Any text or code |

Skills reviewed and rejected for reuse as-is: archify (heavy runtime, writes outside the work area, can edit global agent instructions), coleam00 (no license), design-doc-mermaid (no license file, Mermaid rather than SVG), diagram-design (HTML-first, tiny labels, extra fonts).

## Guidance sources

| Source | License | Used for |
|---|---|---|
| [C4 model notation and checklist](https://c4model.com/diagrams/notation) | CC BY 4.0 | Title/legend/standalone rules, labeled one-way relationships, one zoom level |
| [Agile Modeling style guides](https://agilemodeling.com/style/general.htm) (S. Ambler) | Copyrighted; ideas paraphrased only | Avoid crossings, `?` for unknowns, sequence ordering, black-hole and miracle states |
| [Google developer documentation style guide: images](https://developers.google.com/style/images) | CC BY 4.0 | SVG over PNG, brief text in figures, accessible descriptions |
| [WCAG 2.2 Understanding: use of color, non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color) | W3C document license; ideas only | Color never the sole cue, 4.5:1 text and 3:1 graphics contrast |
| [MDN: SVG in HTML](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_in_HTML) | CC BY-SA 2.5; ideas only | `role="img"`, `<title>`/`<desc>`, `aria-labelledby` |
| [GitHub: theme context for images](https://github.blog/changelog/2022-08-15-specify-theme-context-for-images-in-markdown-ga/) | Ideas only | Dark-mode decision: opaque light card |
| [UML state machine notation](https://www.uml-diagrams.org/state-machine-diagrams.html) | Ideas only | Start dot, end ring, `event [guard] / action` |

## Resources embedded in the skill

| Resource | License | Use |
|---|---|---|
| [Tailwind CSS default palette](https://github.com/tailwindlabs/tailwindcss) (slate, stone, teal, red, amber, orange hex values) | MIT; color values are facts | Role colors in `references/style-guide.md` and `assets/skeleton.svg` |
| Helvetica advance widths from Adobe Core14 AFM metrics | AFM terms permit use for any purpose; only numeric widths reproduced | Text width estimate in `scripts/check_svg.py` |
| Font names: Inter (OFL), Instrument Serif (OFL), Iowan Old Style, Georgia, system fonts | Not bundled; referenced by name in font stacks | Typography |
| Google Chrome / Chromium-family browser | User-installed; invoked locally | `scripts/render_png.py` |

## Decisions

- Hand-written SVG over Mermaid or D2: user choice; full style control, no new dependency. Cost: manual layout, mitigated by the skeleton and checker.
- Hybrid style C over the house style (A) and the diagram-design look (B): user picked after a side-by-side render (`/tmp/diagram-styles/compare.html` at authoring time).
- Diagrams derive from spec/plan; doc links are proposed and applied only after approval (user choice).
- Checker plus render-and-look rather than a checklist only (user choice). Stdlib Python to avoid new dependencies.
- Light theme only; documented limitation.

## Validation (2026-11-23)

- `check_svg.py` on four existing hand-written SVGs from that private work item: flags missing a11y, missing `id="legend"`, diagonal ERD lines, curved connectors, lifelines crossing outcome boxes, 15-box budget overrun. Matches the manual review. Early false "overflow" errors from a flat width estimate and unresolved CSS classes were fixed by Helvetica metrics and class-rule parsing.
- `check_svg.py` on `assets/skeleton.svg` and the corrected example in `references/examples.md`: no errors or warnings.
- `render_png.py` rendered the hybrid sample at 2x with Chrome.
- Trial run: redrew those four diagrams with the skill (brief approved by the user). Each passed the checker; the visual pass found and fixed real defects (tag crowding a cylinder title, a misleading teal arrow, a fragment tab overflowing, a label crossing a lifeline, a cramped sublabel, an unexplained legend item). Checker changes from the run: skip box dividers and `data-role="shape"` outlines in route checks.

## Gaps

- Width estimates can still miss for unusual glyphs or fallback fonts; the visual pass is the backstop.
- No behavioral eval of agents following the brief and approval gates.
