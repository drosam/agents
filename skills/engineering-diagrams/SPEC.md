# Engineering Diagrams Contract

- Intent: produce small, accurate, accessible SVG diagrams that explain a work item's data model, decisions, interactions and lifecycles, derived from the selected spec and plan.
- Inputs: selected `spec.md` / `plan.md` (identity per `docs/work-artifacts.md`), cited ADRs and glossary, code for name verification, or explicit standalone user input.
- Output: `~/.agent-work/<repo-key>/work/<work-id>/diagrams/NN-<slug>.svg` plus `diagrams/README.md` mapping each diagram to its sources. Standalone output goes to a user-named path.
- Modes: Create, Update, Review. Review writes nothing without per-item approval.
- Sequence: identity and sources -> brief (types, questions, sources, cuts, open questions) -> approval when multi-diagram, overwriting or open questions -> draw from `assets/skeleton.svg` -> `check_svg.py` -> render and visual defect pass (max two extra rounds) -> README -> proposed doc-link snippet.
- Style: hybrid house style chosen by the user (2026-11-23): off-white opaque paper, mono eyebrow with type + Work-ID + source sections, serif title, readable sans body (11px minimum, 9px uppercase tags), role colors (new teal, existing slate, decision amber, failure red, external orange) always paired with tags or line styles.
- Safety: never invent facts; mark unknowns with `?`; ask on spec/plan/code conflicts; no edits to spec/plan without approval of the exact snippet; never stage or commit work-area files; scripts are local and non-interactive, with no network access.
- Acceptance: every diagram passes `check_svg.py` without errors; each element traces to a listed source; legend covers every symbol; accessible name present; visual pass names and fixes at least one defect or reports "visual check skipped".
- Files: `SKILL.md` runtime workflow; `references/style-guide.md` tokens and connector rules; `references/diagram-types.md` selection, budgets, notation; `references/examples.md` happy path, robust variant, anti-pattern plus correction; `assets/skeleton.svg`; `scripts/check_svg.py`, `scripts/render_png.py` (Python 3.8+ stdlib; render needs a local Chromium-family browser).
- Limits: text widths are Helvetica-metric estimates; route checks cover axis-aligned segments only; light theme only; static checks do not prove diagrams are correct or that agents follow the workflow.
- Maintenance: update `references/` when style or notation rules change; update `SOURCES.md` with any new source, its license and what was taken; re-run the scripts on `assets/skeleton.svg` and the examples after script changes.
