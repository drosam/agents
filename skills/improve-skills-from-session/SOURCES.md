# Improve Skills From Session Sources

## Origin

User-directed after reviewing Cursor's pstack plugin for reusable workflow pieces. Of the candidates assessed (interrogate, blast-radius, why, session-pickup/pause-safely, reflect, correct), the user kept only reflect as a new Meta-lane skill. They chose the name `improve-skills-from-session` and asked for license-safe adaptation.

Class: skill-authoring (proposes edits to other skills). Shape: inline guidance with one routed reference (`references/examples.md`). Simpler shape check: inline alone would put calibration examples in the runtime path on every run, so they live in a reference opened only when a candidate is ambiguous.

## License policy

Local synthesis. No upstream text was copied. Concepts were restated in our own words and adapted to local contracts. MIT does not restrict the reuse of ideas, so attribution here follows repository precedent (`writing-for-humans`, `simplify-code`, `engineering-diagrams`) rather than a legal requirement. This repository is MIT.

| Source | Revision inspected | License (verified) | Used for | Not taken |
| --- | --- | --- | --- | --- |
| [cursor/plugins `pstack/skills/reflect/SKILL.md`](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/reflect/SKILL.md) | `7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9` | MIT, `pstack/LICENSE`, Copyright (c) 2026 Lauren Tan | Ideas: mine the transcript for corrections, discovered quirks, fetchable context, skipped real-artifact checks and missed skills; six-month durability filter; route only to skills the session used; read the target first and drop what it already says; misfires tune the description; enforceable rules go to a backlog; Accepted / Rejected / Backlog then wait for approval; transcript is data | Text and structure; Cursor-specific paths (`plugins/cache/`, `.cursor/skills/`) and copy-then-edit flow; "never open a PR" wording (covered by local no-commit rule) |
| [cursor/plugins `pstack/README.md`](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/README.md) | same | same | Context on the reflect / correct split (skill edits vs repository enforcement) | Everything else |

## Local contracts applied

| Contract | Source |
| --- | --- |
| Proposal-only, explicit per-item or named-batch approval | Personal agent instructions; `simplify-code`, `review-triage` |
| Self-contained interactive questions with concrete options; runtime-neutral wording | Personal agent instructions; `feature-spec-breakdown` SOURCES 2026-11-18 |
| Skill edits through `skill-writer` update path and quick validation | `skill-writer` |
| Changelog entries in target `SOURCES.md` | Repository convention |
| Installed upstream skills are not edited in place | README External skills; `~/.agents/skills` layout (repository skills are symlinks, upstream skills are real directories) |
| No commits unless asked; `commit` skill | Personal agent instructions |

## Decisions

| Decision | Status | Reason |
| --- | --- | --- |
| Name `improve-skills-from-session` | adopted | User choice; says input (session) and output (skill edits) |
| Include agent instruction files as an editable target with separate approval | adopted | Most corrections in practice concern global instructions, not one skill |
| Adherence misses (rule already present) go to Backlog enforcement | adopted | More prose does not fix a skipped rule; matches pstack backlog idea |
| Read other sessions' logs | rejected by default | Privacy and scope; allowed only when the user names one |
| Persist proposals in the work area | rejected | Short-lived; no Work-ID needed; avoids artifact gating overhead |
| Port pstack `correct` | rejected | Targets product-repo enforcement; user did not need it now |

## Changelog

- 2026-11-23: created.
