# PR Review Sources and Decisions

## Fail-first omissions

User decision: pr-review uses the same fail-first bar as review-triage (see review-triage/SOURCES.md "Fail-first value bar"). Harmless documented misuse and very rare harmless cases are recommended Omit (bucket B) unless they are security issues. When that judgment is uncertain, the item goes to the user (bucket C) rather than being omitted.

## Default decision table

User decisions: pr-review should match review-triage's Table mode (see review-triage/SOURCES.md "Step / Table / Autopilot modes" for research and design), then "pr review should just show the table" with no Autopilot. Outgoing feedback is public wording the user owns, so automatic Keep/Omit is rejected. Mapping: Fix -> Keep, Skip -> Omit, Defer/Discuss -> Investigate. The table is the default with no mode question; Step mode remains available on request or through **Walk everything**. Self-contained `references/decision-table.md` instead of a cross-skill path.

Worker rules shared with review-triage: batching, failure-to-C and main-agent re-check. Probe tests are excluded: the PR head may not be checked out locally, and checking it out would mutate git state outside this workflow.

Unchanged: the earlier rejections of automatic omissions, automatic event choice, pending remote reviews, publication without exact-preview authorization, and comment caps.

Desk cases (expected, not runtime): 12 items -> table, no mode question; `one by one` request -> Step; `go A B` -> C pending; head moves after the table -> affected item back to C; serious race with unverified reachability -> C; table approval never reaches publication without the preview question.

## Whole-review shortlist

User report: pr-review, like review-triage, shortlisted only Findings. Evidence: of three local feedback logs, one surfaced a Coverage spec-scope conflict as an Omit candidate, but a stale plan and a Gaps bullet with four unverified limits went unmentioned. User decision: shortlist every actionable item using review-triage's item kinds and `covered by #M` rule; draft challenges and material gaps as questions to the author; default Omit for gaps/unverified requirements unless the author must act, and for other observations unless the PR touches that code. Keep/Reword/Omit/Investigate and publication gates are unchanged. See review-triage/SOURCES.md "Whole-review queue extraction" for the shared audit.

## Provenance and scope

User approved implementation of a separate outgoing-review skill after research and clarified "Suggestions only" for fixes. Preserve full code-review investigation, offer both direct and existing-report entry points, iterate on important feedback, let the user choose the review event, and publish last only after explicit approval. Persist the source review (code-review default storage, indexes included) plus an append-only feedback/history file.

Class: workflow-process. Selected profile: skill-writer `references/examples/workflow-process-skill.md`. Shape: sequential coordinator using the existing discovery engine; two conditional references for fragile publication and calibration. No additional workers, script, dependency or copied upstream implementation. SPEC.md is a maintenance contract, not a work-artifact spec.

Research observed 2026-11-04. Local reference: session `01a1a6cc-c62d-741d-8e22-68edac878bf2`, named `review <acme-co/acme-shop PR #20205 URL>`, cwd `~/Developer/acme-shop/develop`. Read session messages and draft-writing tool arguments, not a fresh application review. The session narrowed 12 findings to 4 then 2, corrected a stale-record citation and security framing after reachability checks, and needed a separate shortening request. Historical assistant claims are outcome examples, not current application facts. Runtime calibration is synthetic/anonymized; no private code copied.

## Source inventory

| Source | Trust tier / confidence | Contribution and usage constraints |
| --- | --- | --- |
| Current user decisions and selected session above | canonical preference / high for requested behavior; mixed for historical technical claims | Two entry points, full source report, selective concise feedback, suggestion-only fixes, explicit event/publication choice, decision timeline. Revalidate claims, not historical conclusions. |
| Local code-review and review-triage SKILL.md/SPEC.md; Pi SYSTEM.md and README | canonical local / high for contracts | Reuse investigation and evidence standards; narrow only outgoing storage/routing. Incoming fix/commit gates remain. |
| Active Pi executable -> @earendil-works/pi-coding-agent 1.5.0 package; complete docs/skills.md, docs/sessions.md and docs/session-format.md | canonical installed / high for inspected version | Shared skill discovery and reload; JSONL session interpretation. No Pi API integration or executable extension required. |
| https://agentskills.io/specification and https://agentskills.io/skill-creation/best-practices | canonical / high, mutable pages | Portable metadata, coherent workflow, progressive disclosure and grounded examples; no upstream text copied. |
| https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/commands/code-review.md | secondary pattern / high for retrieved text, effectiveness unmeasured; mutable revision | Adopt verified high-signal filtering and one comment per issue. Reject blanket exclusion of input-dependent bugs, tool-success assumptions and implicit publication. |
| https://github.com/feiskyer/claude-code-settings/blob/95dab59a62b2031adcb7abf25ae0a60b8a13fdb2/skills/github-review-pr/SKILL.md | secondary pattern / high for pinned text, effectiveness unmeasured | Adopt batched reviews, evidence/impact separation, stale-head and duplicate-attempt checks. Reject auto-approval/posting, numeric confidence scores, destructive worktree teardown and scope-skipping heuristics. Ideas independently formulated; no source copied. |
| https://github.com/microsoft/powerplatform-build-tools/blob/92c4ebbfe61cae47d27c28cd520f8d4991a11f69/.claude/skills/review/SKILL.md | secondary pattern / high for pinned text | Contrast case: reject "never ask, always decide", automatic submission and arbitrary first-line anchors. No repository-specific rules imported. |
| https://google.github.io/eng-practices/review/reviewer/comments.html | canonical guidance / high, mutable page | Direct respectful comments, explain why, distinguish required/nonblocking. No mandatory praise or solution design. |
| https://docs.github.com/en/rest/pulls/reviews and https://cli.github.com/manual/gh_pr_review | canonical API docs / high, mutable pages | Review events, pinned commit, inline ranges, batched comments, pending-review writes and response handling. No posting executed. |

Public websearch failed with `fetch failed`; read-only `gh search code` and direct source retrieval succeeded. No skills installed. Source collection stopped after these complementary workflows, official publication contracts and the concrete local session covered high-impact decisions and failure recovery; more generic review checklists would add little.

## Adopted, narrowed and rejected

- Add pr-review as the outgoing coordinator; do not duplicate code-review's investigative rubric.
- Leave code-review untouched. A first version added a caller-named `Output mode: pr-review` handoff to skip indexes; review feedback called it coupling for little payoff, and the user accepted indexes as harmless. Routing lives in pr-review's description and the SYSTEM.md authority bullets only.
- Route via descriptions: review-triage's description excludes outgoing reviews; its body is unchanged. SYSTEM.md keeps authority gates plus "ask if ambiguous".
- Keep pr-review SKILL.md short: only rules that change behavior relative to SYSTEM.md/code-review. feedback.md reuses review-triage's triage.md log conventions by reference instead of respecifying them.
- Keep all source findings internally; user-authorized publication selection does not waive a requirement or prove safety.
- Use append-only comment versions and approval snapshots in feedback.md, rather than overwriting drafts or adding index/state files.
- Require independent current-item reachability checks before keeping historical claims. Do not equate UI-only reachability with security or frequency.
- Reject automatic publication, automatic omissions, automatic review-event fallback and hard comment/word caps. Keep suggestions optional and complete; implementation is outside scope.
- 2026-11-19: replaced "Mark nonblocking suggestions as such" with weight-once-in-body. Published reviews (PR #20684, #20352, #20296) prefixed or suffixed every comment with a nonblocking tag even when the body already said so; user found it robotic. Basis: PostHog review handbook (unprefixed = suggestion), GitLab code review guidelines (summary note). Details in writing-for-humans `SOURCES.md`.

## Coverage matrix

| Dimension | Status | Evidence |
| --- | --- | --- |
| Preconditions/context | complete | Explicit target, full selected source, confirmed Work-ID, pinned identity/revisions and relevant discussion |
| Ordered flow | complete | Discovery -> recommended shortlist -> serial decisions/refinement -> event choice -> exact preview -> authorized submission |
| Safety/permissions | complete | Suggestion-only fixes, explicit omission/publication authority, untrusted input, staged artifacts and isolated checks |
| Outputs/acceptance | complete | Full review.md plus append-only feedback.md, stable IDs and snapshots; SPEC checks |
| Failure/recovery | complete | Missing input/tool, stale revision, unavailable checks, anchor/pending-review conflicts, ambiguous submission and failed logging |
| Handoff/resume | complete | Exact selected report, full-log reconstruction and current revision checks |
| Examples | complete | Happy-path short comment, API security guard, corrected overclaim, suggestion boundary and retry/history cases |

This workflow does not teach a general integration API or create other skills; integration/skill-authoring API-depth rubrics are not applicable.

## Trigger checks

Should trigger: "Someone requested my review of this PR"; "draft GitHub feedback for this PR"; "use this code-review report to prepare my review"; "make these outgoing comments shorter"; "publish the approved review draft".

Should not trigger: "audit my local diff exhaustively" (code-review); "fix the comments left on my PR" (review-triage); "debug this crash" (debug); "post a reply to an issue"; "implement this suggested fix" (separate implementation authority).

Description names outgoing intent and both entry points without tying the workflow to a model provider. Ambiguous bare review requests retain code-review discovery; explicit outgoing intent selects pr-review. Desk inspection only, no trigger classifier benchmark.

## Qualitative evaluation

Before/after expectations from guidance inspection, not observed agent runs:

| Case | Expected delta |
| --- | --- |
| Selected session's 12 findings -> short outgoing review | Improved: retain full source, propose exclusions rather than post noise, record user decisions and concise versions |
| Historical claim changes after reachability check | Improved: append explicit correction, preserve ID, reapprove changed wording; no unproved rarity claim |
| Existing review supplied | Improved: reuse exact report without copying; preserve existing files |
| User chooses APPROVE or says "looks good" | Improved: event/content agreement does not authorize publication |
| Head moves after approval | Improved: invalidate approved snapshot, revalidate affected scope, preview and ask again |
| API-only authorization bypass | Unchanged evidence safeguard: serious non-UI issues remain reportable |
| Complete one-line repair versus multi-file repair | Improved: optional complete suggestion versus concise direction, no local mutation |
| Timeout after remote creation | Improved: reconcile exact remote review before retry; no duplicate comments |
| Baseline exhaustive local audit/incoming Fix | Unchanged: code-review and review-triage bodies untouched |
| Preview shown as narration, then "approve the payload above?" (2026-11-18 review-triage negative example: thinking-only entry, no visible text, user could not see the draft) | Improved: item and publication questions carry the complete draft/payload in their own prompt; never a pointer to narration. No runtime-specific field names or size thresholds in the skill |

## Validation results

- `git diff --check -- skills/dot-agents/skills/pr-review skills/dot-agents/skills/code-review skills/dot-agents/skills/review-triage pi/dot-pi/agent/SYSTEM.md`: passed. Separate read-only Python checks covered new untracked files too.
- Dependency-free `python3 -c` structural/preservation checks: passed for name/description subset and limits, required files, routed reference existence, whitespace, runtime path portability, ASCII, balanced fences and five-file new skill. Compared code-review investigation sections 1-5 and review-triage's entire existing workflow body to Git HEAD: unchanged. This is not strict YAML/depth validation.
- `python3 skills/dot-agents/skills/skill-writer/scripts/quick_validate.py skills/dot-agents/skills/pr-review --skill-class workflow-process --strict-depth`: exit 1, `ModuleNotFoundError: No module named 'yaml'`; system Python is 3.9.6, below the declared 3.12+ requirement.
- Retried with existing Python 3.14: `python3.14 skills/dot-agents/skills/skill-writer/scripts/quick_validate.py skills/dot-agents/skills/pr-review --skill-class workflow-process --strict-depth`: same missing-yaml startup failure. Also attempted code-review with `--skill-class security-review --strict-depth` and review-triage with `--skill-class workflow-process --strict-depth` under Python 3.14: same failure. No dependency installed or validator bypassed.
- Installed Pi 1.5.0 CLI smoke command after reading docs/cli.md: `pi --offline --no-extensions --no-mcp --no-skills --skill ./skills/dot-agents/skills/pr-review --no-session --no-approve --help`: exit 0, help printed. This verifies supported invocation flags, not skill discovery or workflow adherence; no extensions or model task executed.
- One read-only focused workflow-contract audit covered direct/reused reports, retention, two-file history, decisions, event/publication separation, stale revisions and recovery. It found an implicit already-published recovery branch; publication reference now explicitly returns the existing URL and stops without POST when an exact submitted snapshot is recovered. No full review or application/GitHub test ran.
- Initial commit `adf5cdf` included a code-review handoff mode and review-triage body paragraph; the follow-up simplification reverted code-review entirely, reduced review-triage to a description change, slimmed SYSTEM.md routing and cut SKILL.md to behavior-changing rules only. Same dependency-free structural checks rerun after the rewrite.

## Open gaps

- Run strict validation in an approved Python 3.12+/PyYAML environment. Missing dependency remains a blocker to a strict-depth pass.
- User created shared and Claude links after implementation; `ls -ld` verified both `~/.agents/skills/pr-review` and `~/.claude/skills/pr-review` point directly to the canonical repository directory. Runtime discovery remains untested: use `/reload` or start a fresh session, with a fresh Pi session required for updated SYSTEM routing. Installed CLI also supports explicit `--skill <canonical-directory>` without persistent registration.
- Exercise direct/existing-review, reword/resume and stale-head/publication recovery in a separately authorized runtime test before claiming adherence.
