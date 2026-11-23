# Examples

Synthetic cases. Use them to calibrate durability and routing, not as templates to copy.

## Happy path: correction becomes a skill edit

Session: the user twice said "ask with options, don't ask in prose" while the agent ran `create-plan`.

```text
Accepted
1. skills/create-plan/SKILL.md - open questions asked in prose
   Evidence: user corrected prose questions in two separate turns.
   Change: in "Open questions", replace "List open questions" with
     "Ask open questions interactively with concrete options; batch related ones."
   Why durable: preference for option-based questions is stable.
```

Approved -> `skill-writer` update path, `SOURCES.md` changelog entry, quick validation.

## Robust variant: misfire becomes a description edit

Session: user said "check the UI on mobile" and the agent did ad-hoc browser clicks; `qa-review` never loaded.

```text
Accepted
1. skills/qa-review/SKILL.md - did not trigger on "check the UI on mobile"
   Evidence: request matched QA intent; skill was not loaded.
   Change: description - add "check the UI", "test on mobile" to trigger phrases.
   Why durable: common phrasing for the same intent.
```

Do not add a body rule like "always use qa-review for UI"; triggering lives in the description.

## Robust variant: enforceable rule goes to Backlog

Session: agent prefixed shell commands with `cd` into the current directory; user corrected it.

```text
Backlog
- "never cd into the cwd" - already in agent instructions; enforce with a
  permission rule that denies `cd <cwd> &&` patterns - owner: permissions file.
```

The rule already exists in prose, so the miss is adherence. More prose will not fix it.

## Robust variant: upstream skill is read-only

Session: `tdd` (installed from an upstream skills repository) suggested a test runner the project does not use.

```text
Backlog
- tdd suggests a generic runner - installed upstream skill, edits would be
  overwritten on update - option: repository agent instructions naming the
  project's test command.
```

## Anti-pattern and correction

Bad:

```text
Accepted
1. skills/debug/SKILL.md - add "the booking spec needs PGPORT=5433 on my
   laptop, see commit 3f9a2c1"
```

Why rejected: machine-specific, includes a SHA, and is a one-off environment fact.

Better:

```text
Rejected
- PGPORT for booking spec - one-off local environment fact.
Backlog
- if this recurs: document the test database port in the project README or
  a setup script that exports it.
```
