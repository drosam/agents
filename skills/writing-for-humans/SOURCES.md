# Writing for Humans Sources and Decisions

## Provenance and scope

User request (2026-11-12): agents write wordy, robotic text on GitHub, GitLab, Linear, Jira and chat; published text should be short, direct, human, keep important data, and may use examples and bullets when needed. Conversation style (the user's terse chat mode) stays unchanged and is not named in the skill. User chose the name `writing-for-humans`, scope (PR/MR comments and replies, PR/MR descriptions, issues/tickets, chat), independent wording with this provenance file, wiring from pr-review, review-triage and feature-spec-breakdown, and synthetic examples informed by public guidance instead of the user's own comments.

Class: generic (writing style). Dimensions chosen: trigger boundary, voice, length, fact preservation, formatting per platform, safety (secrets), examples. Shape: inline-guidance with one routed example reference. Rejected: script-backed (no deterministic transform), hook-backed (provider-specific; posting goes through many CLIs/MCPs; user did not ask for enforcement), router (all text types share one workflow; budgets table covers the differences).

## Source inventory

Research observed 2026-11-12. Public websearch failed (`fetch failed`); skills.sh search API, skills.sh pages, GitHub API and raw files succeeded. Nothing installed.

| Source | Trust tier / confidence | Contribution and constraints |
| --- | --- | --- |
| [blader/humanizer @ b48c832](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/SKILL.md) | secondary pattern / high for retrieved text | AI-tell taxonomy (staging, contrasts, closers, triads, dashes, inflation, chat residue, re-explaining what the reader knows, "When not to act"). Root LICENSE MIT, Siqi Chen 2025. Concepts independently formulated; no text or examples copied. Its own source is Wikipedia "Signs of AI writing" (CC BY-SA); not copied. |
| [hardikpandya/stop-slop @ 8da1f03](https://github.com/hardikpandya/stop-slop/tree/8da1f030185bdfe8471220585162991eaeb970e9) SKILL.md, references/phrases.md, references/structures.md | secondary pattern / high for retrieved text | Filler and throat-clearing lists, false agency, rhythm checks. Root LICENSE MIT, Hardik Pandya 2025. Rejected "kill all adverbs", "no passive ever", "no Wh- openers" and numeric scoring as too rigid for comments. No text copied. |
| [zlliang/skills writing-issues-and-prs @ 39f7d79](https://github.com/zlliang/skills/tree/39f7d799a4c5a823cd24081e98d82d7c3dfdb83f/skills/writing-issues-and-prs) SKILL.md, references/outlines.md | secondary pattern / high | Platform-neutral issue/PR/work-item scope, "fits on one screen", templates win, bug report fields. Repo license MIT (GitHub metadata). Rejected forced Conventional Commits PR titles and formatting micro-rules. No text copied. |
| [Google eng-practices: review comments](https://google.github.io/eng-practices/review/reviewer/comments.html) | canonical guidance / high, mutable | Comment on code not the person, explain why when needed, label severity (Nit/Optional/FYI). CC BY 3.0; ideas only. |
| [Conventional Comments](https://conventionalcomments.org/) | secondary convention / high, mutable | Labels such as nitpick/suggestion/issue and blocking/non-blocking decorations. Adopted only as "use the team's convention if it has one". No text copied. |
| skills.sh results: t3dotgg/tstack `leaving-pr-comments`, vercel-labs `writing-guidelines`, obra `writing-clearly-and-concisely`, miqdadbadjuber `anti-slop`, proseify `anti-prose-slop` | discovery / medium | Compared and not adopted: AI-disclosure banner (user did not ask), doc-review flow, generic Strunk rules, UI-focused or MCP-dependent skills. t3dotgg secret check reflected in the pre-publish checklist. |
| Local pr-review (`SKILL.md` section 3, `references/calibration.md`), review-triage section 6, feature-spec-breakdown section 3 | canonical local / high | Existing draft-style rules stay; new skill supplies shared voice. Their structure, approval and publication gates win. |

Stopping rationale: the two highest-signal humanizer skills, one issue/PR skill and two review-comment conventions cover tells, length, structure and review etiquette. Further generic writing guides repeated the same rules.

## Decisions

- adopted: point first; keep all reader-needed facts; length budgets as defaults, not caps; examples/snippets/bullets allowed when they speed comprehension (user follow-up).
- adopted: explicit "full sentences even if the conversation is terse" rule and a robot-shorthand anti-pattern; generic wording, no mention of the user's chat mode.
- adopted: wording-only boundary; publication authority stays with callers.
- adopted: wiring as one-line pointers in pr-review (draft style), review-triage (section 6 replies) and feature-spec-breakdown (section 3 ticket prose), with the caller's structure taking precedence.
- rejected: vendoring upstream lists (would need MIT notices; user chose independent wording), AI-disclosure banner, hook enforcement, scoring rubric.
- deferred: style mirroring from the user's real comments; add anonymized cases under `references/evidence/` if drafts still miss.

## Coverage matrix

| Dimension | Status | Where |
| --- | --- | --- |
| Trigger boundary | complete | description, Scope |
| Voice and tone | complete | Voice, cut list |
| Length per text type | complete | Length budgets |
| Fact preservation | complete | Workflow step 3, checklist, lossy anti-pattern |
| Platform formatting | partial | Formatting (generic "use target syntax"); no per-tool markup table (Jira wiki/ADF, Slack mrkdwn) |
| Safety | complete | checklist, secrets example |
| Examples | complete | happy path (review comment, reply, PR description, ticket), robust (disagreement, unsure claim, secrets), anti-patterns (lossy, shorthand, wordy) |

## Trigger checks

Should trigger: "reply to the reviewer that it's fixed"; "write the PR description"; "draft a Linear ticket for this bug"; "post a status update in #team"; "this Jira comment sounds like a robot, shorten it"; pr-review drafting inline comments; feature-spec-breakdown writing ticket files.

Should not trigger: "explain this error to me"; "update the README"; "add a comment to this function"; "write the commit message"; "write a blog post about our launch".

Desk inspection only; no trigger classifier run.

## Validation results

- `uv run .../skill-writer/scripts/quick_validate.py skills/writing-for-humans`: blocked by permission policy; not run.
- Manual: name matches directory; description 560 chars, third person; routed `references/examples.md` exists and has Contents (134 lines); SKILL.md 101 lines; `LC_ALL=C grep` found no non-ASCII; `git diff --check` clean; no absolute paths in runtime files.
- Links created 2026-11-12: `~/.agents/skills/writing-for-humans` -> repo dir, `~/.claude/skills/writing-for-humans` -> `~/.agents/skills/writing-for-humans`; both resolve. Runtime discovery untested until reload or new session.

## Changelog

- 2026-11-12: created.
