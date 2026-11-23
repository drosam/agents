---
name: engineering-diagrams
description: Creates, updates and reviews hand-written SVG engineering diagrams (data model/ERD, decision flow, sequence, state/lifecycle, component) for feature work, grounded in the selected spec.md and plan.md when they exist. Use when asked to diagram a spec or plan, draw a data model, sequence, flow or lifecycle diagram, add diagrams to a work item, redo or restyle existing diagrams, or check diagrams against best practices. Applies a house style with accessibility and connector rules, then validates with a check script and a rendered visual pass. Not for UI mockups, marketing illustrations, metric charts, or Mermaid blocks embedded in markdown.
---

# Engineering Diagrams

Turn agreed requirements and design into small, accurate, readable SVG diagrams. Every element traces to a source; nothing is invented to fill space.

## Modes

| Request | Mode | Writes files |
|---|---|---|
| "diagram the plan", "draw the data model" | Create | Yes, after the brief |
| "update diagrams, plan changed", "restyle these" | Update | Yes, after the brief; overwriting needs approval |
| "are these diagrams good?", "check against best practices" | Review | No. Report findings; fix only approved items |

## Step 1: Context and identity

1. Resolve the work area `~/.agent-work/<repo-key>/`: `<repo-key>` is the name of the `git rev-parse --path-format=absolute --git-common-dir` directory, or its parent's name when that is `.git`/`.bare`, without a trailing `.git`.
2. Identify the work item from an explicit user path, current-session confirmation, or a validated reciprocal link. Otherwise ask the user interactively with candidates plus **Other** and **None - standalone**, even with one candidate. Never infer from branch, slug, filename or recency. If asking is impossible, stop and report the blocker.
3. Read the selected `spec.md` and `plan.md`: status, acceptance criteria, non-goals, design sections, plus ADRs and glossary terms they cite. Read existing `diagrams/` files when updating or reviewing.
4. Verify names that appear in diagrams (tables, classes, routes, workers) against code when the repository is available, citing file:line.
5. Spec vs plan conflicts, broken links, or plan vs code mismatches: ask. Do not pick the newer document or quietly "fix" the design in a diagram.
6. No spec or plan: work standalone from code and user input, use `STANDALONE` as the eyebrow source, and ask where to save unless the user gave a path.

## Step 2: Brief before drawing

Open `references/diagram-types.md`. Produce a brief and show it to the user:

```text
Diagram set - <work-id> (spec <status>, plan <status>)
NN <slug> (<type>) - "<reader question>" - <sources: plan 3, 4; spec AC-2; ADR 0002; file:line>
   cuts: <what is deliberately left out or split>
<anything better as a table> -> markdown table, not a diagram
Open: <conflicts, gaps, unknowns>
```

- One question per diagram. Respect the budgets; split over-budget diagrams into overview plus detail.
- Wait for approval when the set has more than one diagram, when it replaces existing files, or when there are open questions. A single explicitly requested diagram with no open questions may proceed after the brief is shown.

## Step 3: Draw

1. Open `references/style-guide.md`. Copy `assets/skeleton.svg` to `<work-area>/work/<work-id>/diagrams/NN-<slug>.svg` and replace the slug prefix in every id.
2. Fill the eyebrow with `TYPE · WORK-ID · <source sections>` and write a subtitle that states the diagram's claim.
3. Every node, label and rule must come from the brief's sources. Unknown facts get `?` and go in the report; never guess.
4. Mark status with fill and a tag (`NEW`, `EXISTING`, `EXTERNAL`, `CHANGED`, `FINAL`). Plan items not yet in code are `NEW`.
5. Lay out on the 4px grid, route orthogonally, then add the legend for exactly the symbols used.

## Step 4: Verify

Run both scripts from the skill directory, one diagram at a time or as a list:

| Script | Arguments | Output | On failure |
|---|---|---|---|
| `scripts/check_svg.py` | `FILE.svg [...]` | JSON per file: `errors`, `warnings`, `stats`; exit 1 on errors | Fix every error. Judge warnings: fix, or state why it is a false positive (width estimates are approximate) |
| `scripts/render_png.py` | `FILE.svg [OUT.png] [--scale N]` | JSON with `png` path in the system temp dir; exit 2 when no browser | Set `CHROME_PATH`, or report "visual check skipped" |

Then view the PNG and name at least one concrete defect (overlap, crowding, ambiguous arrow, unreadable label, misleading color, missing legend item). Fix it by restructuring the layout, not by nudging pixels, and re-render. Stop after two extra rounds. If the same defect survives two attempts, change the approach (split, reorder, switch type). Keep PNGs out of the work directory.

Also confirm against the sources: each acceptance criterion or plan rule the brief listed is visible, and nothing contradicts the spec.

## Step 5: Index and links

Write or update `diagrams/README.md`:

```markdown
# <Feature> - diagrams

**Work-ID:** <work-id>
**Spec:** [spec](../spec.md) (or Not created)
**Plan:** [plan](../plan.md) (or Not created)

| File | Answers | Sources |
|---|---|---|
| [01-data-model.svg](./01-data-model.svg) | What tables does this add? | plan 1, 2, 7; ADR 0002 |

## Editing
Style: engineering-diagrams skill. Check with `check_svg.py`, preview with `render_png.py` or a browser.
```

Propose the exact snippet for linking diagrams from `plan.md` or `spec.md`. Edit those documents only after the user approves that snippet. Never stage or commit work-area files.

## Review mode

Run Step 1, then `check_svg.py` and `render_png.py` on each diagram. Compare against `references/style-guide.md`, `references/diagram-types.md` and the spec/plan. Report findings per diagram as `severity - problem - fix`, covering: source accuracy, one question per diagram, notation for the type, connectors, readability, accessibility, legend, budget. Change files only for items the user approves.

## Report

Reply with: files written, brief changes, checker result per file, the defects found and fixed in the visual pass (or "visual check skipped"), open questions, and the proposed doc-link snippet.

## References

| Open when you need to... | Read |
|---|---|
| pick colors, type sizes, shapes, connector rules, SVG hygiene | `references/style-guide.md` |
| choose a diagram type, check budgets, apply ERD / flow / sequence / state / component notation | `references/diagram-types.md` |
| see a complete brief, conflict handling, or a before/after correction | `references/examples.md` |
| start a new SVG | `assets/skeleton.svg` |
