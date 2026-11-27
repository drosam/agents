# PR Review Contract

## Scope and shape

Workflow-process skill for preparing an outgoing GitHub review with the user. Sequential coordinator: reuse code-review investigation, then user-directed feedback selection and publication. No new discovery workers, scripts, dependencies or scoring systems. Publication details, calibration examples and the default decision table are directly routed references.

Not an incoming-feedback repair workflow. Suggested fixes are prose or complete anchored GitHub suggestions only; no local code changes, commits, pushes, applying suggestions, merge or thread-management authority.

## Inputs and outputs

Inputs: explicit PR target or selected full review, confirmed Work-ID/source identity, pinned revisions, discussion and applicable evidence, user's exact decisions and final publication authorization.

Outputs: full immutable `review.md`; append-only `feedback.md` with stable IDs, proposed dispositions, source locators, evidence corrections, draft versions, exact decisions, recommendation versus chosen event, approved payload snapshot and publication outcomes. A fresh run lets code-review persist normally (indexes included) and adds only `feedback.md` beside `review.md`; an existing complete review is reused without copying.

## Safety and evidence

- Investigate at code-review depth without weakening its evidence, rounds, coverage, source snapshots or technical verdict. Incomplete sources never become complete reviews merely because public feedback is short.
- Verify current-item reachability/impact and counterevidence independently. Preserve API/security concerns, unknown frequency and serious risks. Nits are recommended omissions, not silently discarded findings.
- Require explicit item or batch decisions. The default decision table verifies the whole shortlist first with the same evidence standard. Step mode (serial, one by one) runs only on request or **Walk everything**. No Autopilot. Table workers are read-only, about 5 related items each with at most about 6 at once. A failed or evidence-free verdict goes to C. The main agent re-checks cited evidence before placing an item in A or B. No probe tests. Session continuation waiver is separate from action approval. Keep wording history append-only with actual UTC times and exact decisive inputs; no private reasoning diary.
- Separate acceptance of wording, choice of review event and explicit publication authorization. Bind authority to exact PR/revision/payload; material change requires revalidation and renewed authorization.
- No remote draft creation before authorization. Verify event, diff anchors and remote result; ambiguous attempts require reconciliation before retry. Logging failure blocks publication and never authorizes duplicate posting.
- Preserve WIP, artifact identity, redaction and staged-artifact gates. Missing tools or source/persistence failures are explicit blockers, not permission to guess or bypass controls.

## Acceptance checks

1. Direct PR invocation runs code-review unchanged; this skill adds no mode or input to it.
2. Selected existing report is read fully, retained immutably and checked against current revisions; no repeated full discovery unless changed scope or evidence requires it.
3. Source report retains all supported findings and full coverage/results/gaps. Omission affects public feedback only; it does not resolve technical blockers.
4. A 12-finding source can produce two selected comments without losing the other findings or their disposition history.
5. Keep/Reword/Omit/Investigate controls outgoing feedback; none implies local edits, commits or publication. Suggestions are complete anchored replacements or concise directions.
6. Comments use natural short sentences, normally 1-3, with necessary examples/details; no mandatory report labels, padded praise or repetition.
7. UI, API and crafted-request reachability remain distinct; API-only serious defects are not discarded, and races are not called rare without evidence. Fail first: documented or contract-excluded API misuse where the caller still gets an error, and very rare harmless cases, are recommended Omit unless they are security issues; when that judgment is uncertain the item goes to the user (bucket C), never silently omitted.
8. Recommendation and selected APPROVE/REQUEST_CHANGES/COMMENT remain separate from technical readiness. User chooses; unverified checks do not automatically become blockers or a clean approval.
9. Exact full preview precedes explicit publication and is carried inside the authorization question itself, never only in narration or referenced as "above". "Looks good" and selecting APPROVE alone post nothing. Changed base/head/text/event/relevant discussion invalidates publication approval.
10. Stable IDs and draft versions survive omissions, corrections, restarts and revision changes. Resume reconstructs state from complete source/log, not an index or summary.
11. New runs add only feedback.md beyond what code-review itself writes. Existing files are not migrated; no spec/plan scaffold is required. feedback.md follows review-triage's triage.md log conventions.
12. All decisions, modifiers, material corrections, approved text and publication results are recoverable in timestamp order. Failed appends are never called saved.
13. Batched review uses exact authorized event/commit/body/comments. No own-PR failure fallback, arbitrary anchors, unrelated pending-review submission or blind retry.
14. Closed PR, inaccessible context, failed worker/check, publication error, stale revision and logging failure have explicit stop/recovery paths.
15. The shortlist covers every actionable item in the source review, not only Findings, using review-triage's item kinds and `covered by #M` rule. Challenges are drafted as questions to the author; gaps and unverified requirements default to Omit unless the author must act or answer; other observations default to Omit unless the PR touches that code. Omitting any item is an explicit logged decision.

16. By default, the decision table mirrors review-triage's Table mode: buckets A Keep-sure / B Omit-sure / C your-call, one self-contained table question, reply commands (`go A B`, `walk`, `explain`, `keep`/`omit`/`reword` per item, `reopen`) logged as per-item decisions, unnamed items pending, C paged at 10 rows once it exceeds 15, and no continuation stops for walked items. The table never picks the event, creates a pending remote review or publishes; event choice, exact preview and publication authorization stay separate.

## Validation and limitations

Use the workflow-process strict validator plus desk cases in SOURCES.md and references/calibration.md. Desk checks assess instructions, not model adherence or review accuracy. No GitHub writes or application execution are needed for static validation. Live discovery requires the canonical directory to be exposed to the runtime and reloaded; prompt changes may require a new session. Publication behavior remains untested until exercised with explicit authorization.
