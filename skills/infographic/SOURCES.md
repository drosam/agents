# Infographic Sources

Created: 2026-11-23. Class: workflow-process (artifact generator). Shape: reference-backed workflow with one template asset; no scripts.

Trigger: the user wanted a skill that summarizes a PR, spec, plan, session or any text as one explanatory image for PR descriptions and feature docs. Two renderers were compared side by side on a private work item (hand-written SVG and a paste-ready AI image brief, each as an overview and as a before/after). The user chose to keep both and ask for the renderer per run.

## License policy

Local synthesis. No upstream text, code, scripts or assets were copied; ideas were restated in our own words. Each source's license was checked through the GitHub API. Sources without a license were used for ideas only. This repository is MIT.

## Pattern references (agent skills)

| Source | Revision inspected | License (verified) | Used for | Not taken |
|---|---|---|---|---|
| [patnir411/claude-diagram-skill](https://github.com/patnir411/claude-diagram-skill) `diagram` | `939077e2311eb8be193da12348dd4e8d28b4a50c` | None found | Ideas only: state the one-sentence lesson before designing; pick the visual form from the lesson; quote every string; short isolated labels survive image models; describe zones, not coordinates; check labels after generation | Any text, style or constraint blocks, worked example, script, API calls |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) `infographics` | `c21d13b3cc2894680229ba9959a53281acb9200e` | MIT (GitHub API) | Ideas: layout types chosen by data shape; specific content beats vague prompts; human factual check after any model review; color never the only cue | Text, scripts, OpenRouter pipeline, palettes, scoring thresholds |
| [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer) | `9d5f880b7e8e0a9a80c890b8e1bb6918b68481ad` | MIT (GitHub API) | Ideas: figure-first, the first glance shows the answer; diff and plan summaries as visuals | HTML pages, kit, commands, themes |

## Local reuse

| Resource | Use |
|---|---|
| `engineering-diagrams` skill in this repository | `scripts/render_png.py` for the throwaway preview; SVG accessibility contract (`role`, `title`, `desc`, `aria-labelledby`, opaque background) |
| `docs/work-artifacts.md` | Work-area resolution and spec/plan identity rules |
| Tailwind CSS default palette (MIT; color values are facts) | Role colors in `references/style.md` and `assets/skeleton.svg` |
| Font names Inter (OFL), JetBrains Mono (OFL), system fonts | Referenced by name in font stacks; not bundled |

## Decisions

- Both renderers from one content sheet, renderer asked per run (user choice after the side-by-side comparison).
- Ask only the renderer; the agent picks lesson and layout and shows them in the question context (user choice).
- Brief only, no API call: works with Gemini, ChatGPT or any image model the user prefers (user choice). No new dependency.
- SVG is the deliverable; PNG previews are throwaway (user choice).
- Outputs always in the work area (user choice).
- Brief must be pasteable as-is with no local references (user correction during the comparison).
- No checker script: the `engineering-diagrams` checker enforces orthogonal routing and legends, which do not fit illustrative images. The visual pass and the string trace are the checks.

## Validation (2026-11-23)

- Comparison run on a private approved spec: an overview SVG and a before/after SVG rendered with headless Chrome. The visual pass found collapsed spaces between tspans and fixed them with ` · ` separators; this became a rule in `references/style.md`.
- Both briefs passed the self-containment search after the correction.

## Gaps

- No behavioral eval of agents following the renderer question and the sanitizing rules.
- AI output quality depends on the model the user picks; labels must be checked by hand.
