# Writing for Humans Contract

## Intent

Make agent-drafted text that other people read in collaboration tools short, direct and human, without losing facts the reader needs. Fix the two failure modes the user hits: wordy, robotic prose and over-compressed shorthand.

## Scope

In scope: PR/MR review comments and replies, PR/MR descriptions, issue, ticket and work-item bodies and comments (GitHub, GitLab, Linear, Jira and similar), status updates, chat messages (Slack, Teams and similar).

Out of scope: replies to the user in the current conversation, code comments, documentation files, commit messages, local review/triage logs, and permission to publish.

## Trigger context

- Should trigger: drafting or posting any in-scope text; "make this comment shorter", "this sounds like a robot", "write the PR description", "reply to that thread", "post a status update in Slack"; other skills that draft in-scope text (pr-review, review-triage replies, feature-spec-breakdown tickets).
- Should not trigger: chat answers to the user, README/doc edits, code comments, commit messages, long-form essays or marketing copy.

## Runtime contract

- Switch voice only for the drafted text; the session's conversation style is unchanged.
- Point first; keep every needed fact; cut wording, never data. Examples, snippets and bullets are allowed when they make the text faster to act on.
- Length budgets are defaults; repo, team and tracker templates and the calling skill's structure win.
- Wording guidance only: approval and publication gates stay with the caller and user rules.
- Bundled file loaded at runtime: `references/examples.md`, only for non-comment text types or when a draft still sounds robotic.

## Reference architecture

- `SKILL.md`: scope, workflow, budgets, voice, cut list, formatting, checklist, two core examples.
- `references/examples.md`: per-type before/after examples, robust variants (disagreement, uncertainty, secrets) and two anti-patterns (lossy shortening, robot shorthand).
- `SOURCES.md`: provenance, licenses, decisions, trigger checks, validation.

## Validation

- Structural: frontmatter name matches directory, description length, routed reference exists, ASCII, no absolute paths.
- Desk cases: trigger sets in `SOURCES.md`; each example keeps all reader-needed facts from its "Bad" counterpart.
- Acceptance: a rewritten comment leads with the point, stays within budget or justifies the extra lines with facts, drops all cut-list tells, and keeps every number, name, link and error.

## Known limitations

- Prompt guidance only; no hook enforces it at post time.
- Examples are synthetic. No real comments from the user or third parties are stored.
- English-centric cut list; other languages rely on the general rules.

## Maintenance

- Update `SKILL.md` when a new recurring tell or failure appears in real drafts.
- Store real before/after cases (anonymized) under `references/evidence/` only if iteration needs them; never store secrets or customer data.
- Re-check upstream sources in `SOURCES.md` before adopting new patterns; keep wording independent.
