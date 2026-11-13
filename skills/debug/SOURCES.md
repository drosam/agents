# Debug Sources

## Worktree-shared work area

User-directed storage change: artifacts move from the repository's `.agent-work/` to `~/.agent-work/<repo-key>/`, shared by every worktree of the repository, because removing a worktree deleted its ignored artifacts and work was split across worktrees. `<repo-key>` comes from `git rev-parse --path-format=absolute --git-common-dir` (local, no remote required; bare `~/Developer/acme-shop` -> `acme-shop`); `<work-area>/.repo` guards key collisions. Rejected by the user: per-worktree symlinks, git-config keys and a prompt-injecting Pi extension. Canonical rule: `docs/work-artifacts.md`. Earlier `.agent-work/` paths below are historical.

Retrieved: 2026-09-24. Class: workflow-process; shape: inline investigation.

| Source | Trust tier | Confidence | Usage constraints |
| --- | --- | --- | --- |
| Local history `0bb595144d775cb552208ee559760a2364629e9c` | canonical local | high | Read-only until explicit implementation approval |
| Current user direction | canonical user policy | high | Commands stay read-only except one explicitly requested, one-shot local mutating Rails execution; reset immediately afterward |

Adopt exact-symptom feedback, ranked falsifiable hypotheses, minimal discriminating checks. Preserve safety over a mandatory executable repro. Clarify runner boot, query cost, test side effects, redaction. Narrow the prior mutation prohibition rather than broadly relaxing it: explicit local Rails mutation requests authorize one execution attempt only; implementation approval and prior requests do not carry forward.

Coverage/profile: preconditions, ordered investigation, no-safe-repro recovery, output/evidence and one-shot approval handoff covered. Desk check: local failure → bounded read-only observations; “fix it” → no mutation; explicit targeted local Rails change → one attempt then read-only verification; unsafe runner → ask, not run; no repro → hypothesis labeled. Negative trigger: production command execution.

Stop: relevant diagnostic pattern and local restrictions reconcile the change. Gap: original source unknown; retrieve owner-provided provenance if needed. Strict validator blocked by missing PyYAML; no application runtime executed.
