# Production Debug Sources

## Worktree-shared work area

User-directed storage change: artifacts move from the repository's `.agent-work/` to `~/.agent-work/<repo-key>/`, shared by every worktree of the repository, because removing a worktree deleted its ignored artifacts and work was split across worktrees. `<repo-key>` comes from `git rev-parse --path-format=absolute --git-common-dir` (local, no remote required; bare `~/Developer/acme-shop` -> `acme-shop`); `<work-area>/.repo` guards key collisions. Rejected by the user: per-worktree symlinks, git-config keys and a prompt-injecting Pi extension. Canonical rule: `docs/work-artifacts.md`. Earlier `.agent-work/` paths below are historical.

Retrieved: 2026-09-24. Class: workflow-process; shape: read-only analysis + user-run handoff.

| Source | Trust tier | Confidence | Usage constraints |
| --- | --- | --- | --- |
| Local history `0bb595144d775cb552208ee559760a2364629e9c` | canonical local | high | Never execute production Rails commands or mutations |
| Current user direction | canonical user policy | high | Commands stay read-only except one explicitly requested mutating Rails copy/paste handoff; reset immediately afterward |

Decision: preserve assistant execution only for approved read-only production tools; preserve user-run Rails commands. Narrow the prior generation prohibition rather than broadly relaxing it: an explicit request for one specific mutating production Rails command authorizes one clipboard handoff only, never execution, and permission does not carry forward. Keep environment/result bounds, redaction, and clipboard fallback explicit.

Coverage/profile: workflow context, observation flow, permission safety, clipboard failure, result handoff covered. Desk cases: pasted incident log → local analysis; generic “fix it” → no mutation payload; explicit targeted Rails repair request → one handoff then read-only; unavailable clipboard → fenced payload once, no false copied claim. Code approval never becomes production mutation approval.

Stop: local safety contract and bounded diagnostic pattern cover relevant deltas. Gap: original upstream unrecorded; request original URL if needed. Strict validator blocked by missing PyYAML; no production actions tested.
