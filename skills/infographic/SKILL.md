---
name: infographic
description: Creates a one-image visual summary (infographic) of a pull request, a feature spec or plan, the current session, or any pasted text or topic, as a hand-written SVG, a paste-ready prompt for an AI image model (Gemini, ChatGPT or any other), or both. Use when asked to make an infographic, a visual summary, an explainer image, "a picture worth a thousand words", an image for a PR description, or to visually summarize a PR, spec, plan, session, feature or idea. Not for multi-diagram engineering sets (engineering-diagrams), UI mockups, metric charts or slide decks.
---

# Infographic

Turn one source into one 16:9 image that teaches its main point in five seconds. Same content sheet drives both renderers, so the SVG and the AI image say the same thing.

## Step 1: Read the source

| Input | Read |
|---|---|
| PR number, URL or branch | `gh pr view <n> --json title,body,files` and `gh pr diff <n>`; for a local branch, `git log` and `git diff <base>...HEAD` |
| Spec or plan | The user-named file, or one confirmed this session or reached by a validated reciprocal link. Otherwise ask with candidates plus **Other** and **None - standalone**; never infer from branch, slug or recency. Read status, problem, solution, decisions, non-goals |
| Current session | Only what happened in this conversation: goal, decisions, changes, outcome, open items |
| Pasted text or topic | Use as given. No research unless asked |

Unclear source: ask. Do not summarize from memory of other sessions.

## Step 2: Write the content sheet

Open `references/layouts.md`. Draft, without asking the user:

```text
Lesson:   <one sentence the reader must get in 5 seconds>
Layout:   <pattern from layouts.md> - <why it fits>
Title:    "<= 6 words"   Subtitle: "<optional, <= 12 words>"
Zones:    <zone>: "<exact string>", "<exact string>", ... (objects to draw)
Example:  <concrete values: real names, states, numbers, sample rows>
Takeaway: "<one line>"
Cut:      <what was left out and why>
```

- Every string traces to the source. Unknown: leave it out, never guess.
- Budget: about 40 short strings total; labels up to 6 words; lines up to 45 characters. Prefer drawn objects (windows, envelopes, tables, timelines) over sentences.
- At least one concrete example per zone; it makes the image read as real, not as a template.
- Sanitize: no secrets, tokens, internal hostnames, customer names, emails or IDs. Use obvious placeholders (`jane@example.com`, `Customer A`, `#1234`) and list them in the report.
- Too much for one image: keep the one story that matches the lesson and offer a second image for the rest.

## Step 3: Ask for the renderer

Ask one question with the question tool; skip it only when the user already named the renderer. Put the lesson, layout, title and zone outline in the question context so the user sees the plan. Options:

- **Both (Recommended)**: SVG plus a paste-ready AI image brief from the same sheet
- **SVG**: exact text, editable, no external tool
- **AI image brief**: richer illustration; the user pastes it into Gemini, ChatGPT or another image model

Render nothing before the answer.

## Step 4: Render

Output folder, in the work area `~/.agent-work/<repo-key>/` (resolve `<repo-key>` from `git rev-parse --path-format=absolute --git-common-dir`: its name, or its parent's name when it is `.git`/`.bare`, without `.git`):

| Source | Folder |
|---|---|
| Selected spec or plan | `work/<work-id>/infographic/` |
| PR | `work/pr-<number>-<short-slug>/infographic/` |
| Session | `work/session-<yyyy-mm-dd>-<topic>/infographic/` |
| Text or topic | `work/<topic-slug>/infographic/` |

Outside a Git repository, ask for a path. Never overwrite an existing file without asking; suggest a `-2` suffix. Files: `<name>.svg` and `<name>-brief.md`, where `<name>` is a short kebab slug of the title or layout.

| Renderer | Do |
|---|---|
| SVG | Open `references/style.md`. Start from `assets/skeleton.svg`. The SVG is the deliverable. To look at it, render a throwaway preview in the temp dir (commands in `references/style.md`); never save or deliver a PNG. Name and fix concrete defects: overlap, clipping, collapsed spaces, crowding, unclear arrows. Stop after two extra rounds; if a defect survives, change the layout |
| AI image brief | Open `references/brief.md` and fill its template. The whole file is the prompt: no headings, notes, links or paths around it |

## Step 5: Verify

- Every string in the SVG or brief is in the content sheet, and the sheet traces to the source.
- Search the brief for local paths, file names of source docs, repo paths, work IDs, private URLs and phrases like "see the spec" or "attached plan". None may remain; the model cannot see them.
- No sensitive data; placeholders are obvious.
- SVG preview was viewed, or report "visual check skipped" with the reason.

## Step 6: Report

Reply with: files written, lesson, layout, defects found and fixed, and placeholders used. Then:

- Brief: paste the whole file into the image model and ask for 16:9. Check every label afterwards against the content sheet; for garbled text ask the model to change only that label, or regenerate.
- A markdown snippet to paste: `![<lesson as alt text>](<image URL after upload>)`.

Never edit a PR body, spec or plan unless the user asks. Never stage or commit work-area files.

## References

| Open when you need to... | Read |
|---|---|
| pick a layout pattern and its zones and budgets | `references/layouts.md` |
| apply palette, type, shapes, icons and SVG rules, or render the preview | `references/style.md` |
| write the paste-ready AI image brief | `references/brief.md` |
| see a full content sheet, a sanitized variant, or a bad brief corrected | `references/examples.md` |
| start a new SVG | `assets/skeleton.svg` |
