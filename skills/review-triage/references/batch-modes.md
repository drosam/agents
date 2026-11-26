# Table and Autopilot modes

Open when the user picked **Table** or **Autopilot** for this triage session. Evidence rules, item kinds, persistence, validation, commit and safety gates from `SKILL.md` still apply. Only the order of work and how decisions are gathered change.

## 1. Investigate the whole queue first

- Before any edit, investigate every pending item with `SKILL.md` sections 2-3, in queue order. Use the same evidence standard as Step mode. Severity labels, round counts and reviewer confidence never shorten verification.
- Workers (below) may investigate in parallel. Probe tests (below) may confirm or disprove claims.
- Keep `covered by #M` links. A covered item takes its bucket from #M's outcome.
- Append one dense line per item to `triage.md` before showing anything: `- <UTC> #N bucket A|B|C; rec: <action> - <smallest fix | residual | check>; evidence: <path:line>; probe: <cmd -> result | none>; unknowns: <...>`.

### Workers

- **Batch:** group pending items by file or area, about 5 per worker, with at most about 6 workers running at once. Items sharing code go to the same worker, so it reads that code once.
- **Input:** pinned identity, target SHA, each item's `review.md` source range, the section 2-3 rules and the probe rules below.
- **Output per item:** verdict class, likelihood with its trigger, impact, smallest fix, decisive `path:line` evidence, unknowns, and the path of any drafted probe with its run command.
- **Access:** workers read code, search, read git history and run existing tests that change nothing. They write only probe drafts in the work area. They never edit repository files, run probes, change git state or commit. Use a cheap read-only worker type for reading. A worker that drafts probes needs write access to the work area.
- **Failure:** if a worker crashes, times out, skips an item, or returns a verdict without `path:line` evidence, the item goes to C as `worker failed: <reason>`. Never put it in A or B on a guess.
- **Re-check:** before placing an item in A or B, open its cited `path:line` and any probe result and confirm they support the verdict. Otherwise the item goes to C.

### Probe tests

A probe is a throwaway test that checks whether a claim really happens. It never fixes anything.

1. A worker (or the main agent) drafts the probe at `<review dir>/probes/<N>-<slug>.<ext>`, beside `triage.md`, following the project's test conventions.
2. Only the main agent runs probes, **one at a time**, after recording `git status` so existing work is known.
3. To run a probe, copy it into the project's test directory under a new unique name (`triage_probe_<N>_...`). Never overwrite or edit an existing file. Run only that test, then delete the copy and confirm `git status` no longer shows it. If cleanup fails, stop and report a blocker.
4. Log `#N probe: <cmd> -> <result>`. A probe that fails to run (syntax or setup) gets one repair attempt. If it still fails, the item goes to C as `probe inconclusive`.
5. **Reproduces the claim** (the test fails as the claim predicts): keep the draft in `probes/` for the fix step and log its path. **Disproves the claim:** log the command and result, then remove the draft from `probes/`.
6. Never touch production, start servers, install dependencies, run migrations outside the test database, or cause network side effects. A probe that would need any of these is not run; the item goes to C with the needed check named.

## 2. Buckets

| Bucket | Put an item here when | Recommendation |
| --- | --- | --- |
| **A - Fix, sure** | Confirmed defect or supported improvement. The smallest fix is clear, fits this branch's purpose and needs no further decision. Also a `gap`/`req` item with a permitted read-only check | Fix / Fix here / Adopt (small) / Run check |
| **B - Skip, sure** | Verified not applicable or unreachable, already resolved, AI slop, or a verified rare edge with low impact under section 3. Never security/privacy, data loss, financial integrity or a mandatory contract | Skip / Keep current / Accept gap |
| **C - Your call** | Everything else: unverified claims or unknown frequency, tradeoffs, `C-*` challenges, spec/plan/docs edits, Ticket versus Fix here, review-induced churn, fixes that need broader work, and any Defer recommendation | Item's own actions, recommendation first |

A confirmed serious defect goes in A even when its frequency is unknown. A serious claim that is still unverified goes in C. When a choice between buckets is unclear, use C.

## 3. Present one table, ask once

Persist the full table in `triage.md`, then ask one self-contained question containing it:

```markdown
### Triage table - <total> items: A <n> fix, B <n> skip, C <n> your call

**A - Fix, sure**
- #3 P2 `app/x.rb:42` - Nil total on empty cart - Fix: default to 0 - `app/x.rb:42`, `spec/x_spec.rb:10`
- ...

**B - Skip, sure**
- #5 P3 `app/y.rb:8` - Extra guard request - Skip: caller validates at `app/z.rb:20` (AI slop)
- ...

**C - Your call** (page 1 of 2)
- #9 C-approach - Use job instead of polling - rec: Keep current
  Polling runs every 30s for at most 5 users (`app/poll.rb:12`). A job adds a queue and retry states for little gain.
- ...

Reply: `go A B` · `walk C` / `walk 4 9` · `explain 12` · `12 skip` · `7 fix but keep name` · `defer 3`
```

- A and B rows are one line each. Each C row adds at most two short sentences of context and verdict. Never copy original feedback into the table. `explain N` shows it.
- When C has more than 15 rows, show 10 per page. A and B are always shown in full.
- Options, recommendation first: **Apply A + B, walk C**, **Apply A + B, defer C**, **Walk everything** (switch to Step). A custom answer takes the reply commands.
- Log the exact reply. Turn it into one decision event per named item, for example `#3 decision: Fix; input: "go A B"`. Items the reply does not name stay **pending** and are never fixed. If part of the reply is ambiguous, log Discuss for only the affected items and ask about that part.
- `explain N` shows the full Step card for item N (section 4 A format) with N's actions plus **Back to table**. Choosing **Back to table** decides nothing.
- `reopen N` moves an auto-skipped or decided item back to C as pending.

## 4. Execute approved work

1. Process approved items in queue order. Items sharing one root cause and one smallest fix form a single group with a single commit.
2. Before each group, re-check the current code, because earlier fixes may have changed it. If an item no longer applies, or its fix grows past the agreed smallest change, stop that item, return it to C as pending and give the reason.
3. Validate each group with the section 5 **Fix** rules: the regression test fails before the fix and passes after it, plus focused checks. When an item has a saved probe, start the regression test from it, renamed and placed per project conventions. If validation fails, undo only this group's uncommitted changes and keep unrelated work. Log the group as blocked and move on to the next group.
4. Commit each validated group through the `commit` skill. Log the hash once with every item number it covers: `#3 #7 fixed: <root cause>; <cmd -> result>; <hash>`.
5. Log skips and defers per item. Run approved checks. If a check exposes a defect, the item returns to C with a new assessment.
6. Do not stop for continuation between items. Choosing the mode already waived those stops for this session. Logging and serial execution stay mandatory.
7. Then walk the named items Step-style: re-investigate against the updated code, use the section 4 card and section 5 decisions, with no continuation stops.
8. End with a compact report, `#N | outcome | commit | note`, with one line per item handled this run. Then ask about any items still pending: **Walk them**, **Defer all** or **Leave pending** (Active triage stays pinned). Ask nothing when none remain.

## 5. Autopilot

Autopilot runs sections 1-2, then acts without asking on rows that pass the **Moderate bar** below. Everything else is parked as pending, never fixed.

| Row | Autopilot action |
| --- | --- |
| A, confirmed serious: P0/P1, security/privacy, data loss, financial integrity, broken mandatory requirement/contract | Auto-fix when the fix stays within the size limits below; otherwise park |
| A, confirmed defect with a `common` or `uncommon` trigger, and the smallest fix stays within the size limits | Auto-fix |
| A, `gap`/`req` with a permitted read-only check | Run it. Pass: close. Defect: bucket the result again under these rules |
| B | Auto-skip, logging the evidence and the accepted residual behavior |
| Anything else: P3 polish, `very rare`/`unknown` trigger, C rows, Ticket, docs/spec/plan edits, Adopt/Cut scope, review-induced churn, oversized fixes | Park |

- **Size limits:** about 20 changed lines excluding tests, at most 2 non-test files, no new state, flag, fallback or guard layer, no public API/schema/migration/config change, and within the branch's purpose.
- When unsure, park. Never fix "to be safe".
- Cap: at most 8 auto-fixed items per run. Once the cap is reached, park the remaining eligible rows in A for approval.
- Autopilot never pushes, replies on the code host, edits a spec/plan, creates a tracker issue, installs dependencies or starts servers.
- Log auto decisions as `#N decision: Fix (autopilot, Moderate: <criterion>); input: "<exact mode-choice message>"` or `Skip (autopilot, ...)`.
- Execute with section 4 steps 1-6. Then report everything auto-fixed (with commits), auto-skipped (with reasons) and checked, plus the parked items as a Table-mode table and question (section 3). Auto-skipped rows stay listed so the user can `reopen N`.

## 6. Mode lifetime

- The mode lasts for the current triage session. `step`, `table` or `autopilot` switches mode for the remaining pending items; log the switch as a session-control event.
- A fresh session asks again. Earlier auto decisions remain logged decisions.
- Completion, persistence-failure, Discuss and handover rules from `SKILL.md` are unchanged.

## Examples

- **Happy path:** 38 items. The table has A 14, B 16, C 8. The user replies `go A B, walk C`. 14 fixes are grouped into 9 root-cause commits. 16 skips are logged. Then the 8 C items are walked Step-style. Report, then nothing pending.
- **Robust variant:** item #7 is in A, but by execution time an earlier commit has removed its code path. Return it to C with the reason; do not invent a new fix. Group #11 fails its regression test. Undo only that group, log it blocked, continue, and list it in the report.
- **Anti-pattern:** Autopilot adds a retry fallback for a `very rare` race with unknown impact, because the change is "only 10 lines". **Correct:** a `very rare` or `unknown` trigger always parks, whatever the fix size. Only verified rare and low-impact rows auto-skip; serious unverified rows park in C with their settling check.
