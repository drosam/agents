# Create Plan Sources

## Worktree-shared work area

User-directed storage change: artifacts move from the repository's `.agent-work/` to `~/.agent-work/<repo-key>/`, shared by every worktree of the repository, because removing a worktree deleted its ignored artifacts and work was split across worktrees. `<repo-key>` comes from `git rev-parse --path-format=absolute --git-common-dir` (local, no remote required; bare `~/Developer/acme-shop` -> `acme-shop`); `<work-area>/.repo` guards key collisions. Rejected by the user: per-worktree symlinks, git-config keys and a prompt-injecting Pi extension. Canonical rule: `docs/work-artifacts.md`. Earlier `.agent-work/` paths below are historical.

## Later local work-area contract

User-directed destination change: `.agent-work/work/<work-id>/plan.md` supersedes `docs/design/`. The user subsequently chose work-first grouping with sibling `spec.md` and reciprocal local links. Add Work-ID/status, explicit reciprocal spec/plan links, user-confirmed identity across sessions and blocked-pairing handling. Preserve research/findings/walkthrough and separate implementation approval. Historical destination-preservation notes below describe the prior refresh, not current policy.

Retrieved: 2026-09-24. Class: workflow-process; shape: phased plan/validate workflow.

| Source | Trust tier | Confidence | Usage constraints |
| --- | --- | --- | --- |
| Local skill and history `f1ff2f87ff72e170bf897326c1a6f60b64cc308e` | canonical local | high | Preserve research/findings/doc/walkthrough/approval phases |
| https://github.com/getsentry/skills/tree/c2f99a5b04b4cd992ec3022d7c2c3e23e938d241/skills/skill-writer | secondary authoring patterns | high | Guidance only; not claimed as original create-plan source |

Decision: narrow unsolicited activation, permit bounded direct reads on denied delegation, distinguish design acceptance from implementation authority. Preserve output destination and one-step walkthrough.

Coverage/profile: workflow preconditions, phases, fallback, safety and handoff covered; inline template and good/bad interaction examples retained. Desk checks: research request → findings before file; review complete → no code; blocked worker → direct reads or explicit gap. Negative trigger: already-approved small fix.

Stop: local process is authoritative; generic planning searches would not establish lineage. Gap: exact original unrecorded; ask owner for URL before claiming upstream synchronization. Strict validator blocked by missing PyYAML; no behavioral benchmark.
