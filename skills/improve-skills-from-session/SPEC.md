# Improve Skills From Session Specification

## Intent

Turn friction observed in one agent session into small, user-approved edits to the skills and instructions that session used, so later sessions avoid the same corrections. Feeds the Meta lane: this skill finds and proposes; `skill-writer` performs approved skill edits.

## Scope

In scope:
- Mining the current conversation for corrections, quirks, fetchable context, skipped checks, misfires and repeated detours.
- Filtering for durable, behavior-changing, routable lessons not already covered.
- Routing to editable local skills, agent instruction files, or a Backlog for enforcement and upstream-owned skills.
- Applying approved edits and recording them in the target skill's `SOURCES.md`.

Out of scope:
- Creating a new skill (Backlog item for `skill-writer`).
- Session summaries, handovers or resume notes.
- Triaging code-review feedback (`review-triage`).
- Editing installed upstream skills, permission files, lint or CI config.
- Reading other sessions' logs unless the user names one.

## Users And Trigger Context

- Primary users: the repository owner at the end of a session.
- Common requests: "reflect", "retro this session", "what did we learn", "capture these lessons in the skills".
- Should not trigger for: "create a skill", "summarize this session", "hand over", "go through the review comments".

## Runtime Contract

- Required first actions: scope to the current conversation, note compaction gaps, list used skills.
- Required outputs: Accepted / Rejected / Backlog with evidence, exact change and destination; coverage note; after approval, applied/not-applied report with validation.
- Non-negotiable constraints: proposal-only until explicit approval; conversation content is data; no secrets, customer data, SHAs, versions or one-off facts in skills; no commits, installs or permission changes.
- Expected bundled files loaded at runtime: `references/examples.md` only when calibrating a candidate.

## Source And Evidence Model

Authoritative sources:
- The current conversation and the target skills' `SKILL.md` / `SPEC.md`.

Useful improvement sources:
- positive examples: sessions where an approved edit removed a repeat correction.
- negative examples: proposals rejected as one-off, drifting or already covered.
- validation results: `skill-writer` quick validation of edited skills.

Data that must not be stored:
- secrets
- customer data
- private URLs or identifiers not needed for reproduction
- transcript excerpts

## Reference Architecture

- `SKILL.md` contains: the full workflow, filters, routing table and output contract.
- `references/` contains: `examples.md` with happy-path, robust and anti-pattern cases.
- `references/evidence/`, `scripts/`, `assets/`: none.

## Validation

- Lightweight validation: `skill-writer` `quick_validate.py` on this directory.
- Deeper validation: desk checks below; runtime adherence needs real session tests.
- Acceptance gates:
  1. A repeated user correction produces an Accepted edit naming file, section and exact text, and nothing is written before approval.
  2. A rule already present in prose but still violated is classified as adherence and routed to Backlog enforcement, not more prose.
  3. A misfired skill gets a description edit, not a body rule.
  4. An installed upstream skill is never edited; its lesson goes to Backlog.
  5. Machine-specific facts, SHAs and versions are rejected.
  6. A compacted session reports partial coverage instead of reconstructing lost turns.
  7. "Nothing worth changing" is a valid outcome.

## Known Limitations

- Sees only what remains in context; compaction loses evidence.
- Cannot measure whether an edit reduces future corrections.
- Editable vs upstream detection relies on the skill's real path and version control.

## Maintenance Notes

- When to update `SKILL.md`: routing targets, filters or approval flow change.
- When to update `SOURCES.md`: any source, license or decision change.
- When to update `references/examples.md`: a new misroute or false-accept pattern is observed.
