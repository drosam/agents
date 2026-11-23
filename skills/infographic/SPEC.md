# Infographic Contract

- Intent: summarize one source (PR, feature spec or plan, current session, pasted text or topic) as one 16:9 image that teaches its main point in five seconds.
- Inputs: PR via `gh` or local git diff; spec/plan selected per `docs/work-artifacts.md` identity rules; the current conversation; user text.
- Outputs: `<name>.svg` and/or `<name>-brief.md` in `~/.agent-work/<repo-key>/work/<work-id or slug>/infographic/`. The SVG is the deliverable; previews are throwaway temp files. The brief file is the whole prompt, pasteable into any image model.
- Sequence: read source -> content sheet (lesson, layout, exact strings, example values, takeaway, cuts) -> one question: renderer (both / SVG / brief) -> render from the same sheet -> verify -> report with a markdown snippet.
- Asking: only the renderer, unless the user already named it; source selection questions follow the work-artifact rules. Lesson and layout are shown in the question context, not asked.
- Style: flat editorial infographic, soft pastel role colors, rounded cards, line icons, 1600x900 canvas; tokens in `references/style.md`. Layout patterns in `references/layouts.md`.
- Safety: every string traces to the source; unknowns are left out; secrets, tokens, internal hosts and customer data are replaced by obvious placeholders and reported; the brief contains no local paths, file names, work IDs, private URLs or references to unseen documents; no overwriting without asking; no edits to PR bodies, specs or plans unless asked; never stage or commit work-area files.
- Acceptance: content sheet produced before rendering; renderer asked once; SVG self-contained with `role="img"`, title, desc and opaque background, viewed in a preview with defects fixed or "visual check skipped" reported; brief passes the self-containment search; both outputs carry the same strings.
- Files: `SKILL.md` runtime workflow; `references/layouts.md`; `references/style.md` (tokens, SVG rules, preview commands); `references/brief.md` (rules, template, model notes); `references/examples.md` (happy path, robust variant, anti-pattern plus correction); `assets/skeleton.svg`.
- Dependencies: none new. Preview uses the sibling `engineering-diagrams/scripts/render_png.py` or a local Chromium-family browser. AI rendering is manual: the user pastes the brief.
- Limits: no automatic image-model call; AI images can garble text and need a manual label check; SVG text widths are estimated; light theme only.
- Maintenance: keep layouts and style tokens in sync with the brief template; record new sources and licenses in `SOURCES.md`; do not copy text from sources without a compatible license.
