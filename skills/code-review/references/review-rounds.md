# Review Rounds

Read this file immediately before dispatching review workers. A round is an independent sample of every applicable review role, not a new review dimension or a refinement of an earlier result.

## 1. Select the round count and roles

- An explicit `rounds=N` or equivalent request wins. Accept only integers from 1 through 3. For an invalid explicit value, stop and ask for a valid value; never clamp it silently.
- A quick full-dimension review or an explicitly narrowed review uses 1 round unless the user supplies another valid count.
- Every other review uses 2 rounds by default. Do not ask for confirmation.
- Use 3 rounds only when explicitly requested. Diff size changes scope partitioning, not the sample count.

Each full round runs these roles:

- the four review dimensions (section 2)
- one intent-blind worker (section 3)
- one whole-change simplicity worker (section 4)
- one approach worker (section 5)
- one spec worker, only when a requirements source exists (section 6)

A quick full-dimension review keeps every role. An explicitly narrowed review runs only the applicable dimensions and excludes blind, simplicity, approach and spec unless the user explicitly includes them.

### Round models

Different models miss different issues, so later rounds may use another model. This applies only when the count is 2 or more and the runtime lets the coordinator choose a model per worker.

- If the request already assigns models (for example `R2 on <model>`), use them without asking.
- Otherwise ask one single-select question before dispatch. Options: **Same model for all rounds** (the current model) and **Different model for later rounds**. A custom answer names the model per round, for example `R2: <model>`.
- If the runtime cannot choose a model per worker, do not ask. Run every round on the current model and record `round models: unsupported - one model`.
- Every worker in a round uses that round's model, including blind, simplicity, approach and spec. The coordinator's single-run work (spec mapping, docs/history, checks, claim verification and synthesis) stays on the current model.
- Log the choice with the run, and print it in the preflight below.

Before dispatch, print the selected count and cost. For a full review use this shape:

```text
Review rounds: <N>
Round models: R1 <model> | R2 <model> | ... (or: one model: <model>)
Discovery workers: <8N with spec | 7N without>
- <N> x 4 review dimensions
- <N> x intent-blind
- <N> x simplicity
- <N> x approach
- <N> x spec | spec: n/a - no requirements source
Single-run work: spec mapping, docs/history, checks, verification
```

For an explicitly narrowed review, list only the applicable roles and total, and name excluded roles. Start after printing; do not request another confirmation.

## 2. Prepare shared inputs once

The coordinator owns scope, requirements, rules, documentation, history, deployment context and validation inventory. Resolve them once, then give every sampled worker the same immutable target and the evidence packet allowed for its role. Do not repeat spec discovery, documentation/history collection, static checks or deployment lookup per round.

Use these four dimensions in every full round:

| Dimension | Preferred agent if available | Required focus |
| --- | --- | --- |
| Behavior/spec/edge cases | `code-review-behavior` | Requirements, wiring, state transitions, callers and input-dependent failures |
| Security/data/rollout | `code-review-security` | Reachable threats, tenant boundaries, persistence, migration, deployed-version coexistence, devex and feature-gate leaks |
| Tests/reliability/performance | `code-review-tests` | Behavioral test validity, failure handling, concurrency, resource limits and operational evidence |
| Rules/docs/patterns/code health | `code-review-code-health` | Scoped rules, best practices, doc consistency, recent precedents, ownership, invariants and structural simplification |

Tag every task with its round and role, for example `R1 behavior`, `R2 security`, `R1 blind`, `R2 approach`. When rounds use different models, the tag also names the model, for example `R2 behavior [<model>]`. General workers receive the complete analytical rubric, not only the role name. Specialized workers cover their entire row. Pass the resolved skill path and relevant contract/rubric text, but state that shared validation execution remains coordinator-owned. Sampled workers inspect test code and CI evidence and propose discriminating checks; they do not run repository test/lint/typecheck/build commands or browser flows during discovery. Workers never spawn nested workers.

Include the added checks in their existing dimension packets without omitting any current focus: code health returns canonical reuse candidates, semantic differences and producer/consumer contract traces; behavior and tests return relevant same-identity repeat-action and pending/settled scenarios with discriminating assertions. A bare `consistent`/`checked` label is not that evidence. Use explicit inapplicability or an exact source/access gap when needed. These are deeper checks in the same four dimensions, not extra workers.

Each sampled dimension worker receives the exact target/commit IDs, local-change inventory when applicable, confirmed Work-ID and selected documents, relevant rules/spec/docs, comparison sources and this return contract:

```text
Read-only review; no nested workers. This is independent sample <round>/<total>,
<dimension>. Do not inspect another worker's findings. Inspect beyond the diff
when necessary. Return all supported findings with path:line, trigger, impact,
evidence, counterevidence, fix direction, and regression-check suggestion.
Return checked/not-applicable/unchecked coverage with reasons and sources.
Do not assume another worker covers an omitted risk. Identify tool failures.
Do not execute shared validation commands or browser flows; propose checks for
coordinator verification after claim deduplication.
```

Launch every worker for every round in parallel in one tool turn when capacity permits. Otherwise use bounded waves without exposing completed findings to workers that have not started. Independent sampling is lost if a later round receives earlier findings or is asked merely to confirm them.

## 3. Run one intent-blind worker per round

Run one `code-review-blind` worker in each round of every full review, including a quick full-dimension review. Exclude it from an explicitly narrowed review unless the user explicitly includes it. Give each blind sample the same pinned diff/content scope, applicable repository rules, safety/evidence/severity contract and output schema. Filter selected spec/plan/ticket paths and other intent documents out of the supplied diff/content command before launch; if reliable filtering is impossible, mark blind coverage unchecked instead of exposing them. Pass the minimum work identity required by the active harness: Work-ID, status and selected document paths labeled `identity only - do not read`. Withhold document contents, user requirements, decisions, tickets, PR description/discussion, commit-message rationale, coordinator interpretation and all other findings, including other blind samples. Tell it not to inspect those sources.

The blind worker judges implementation behavior without author intent. It does not replace requirement fidelity and cannot decide whether unspecified behavior violates the spec. Reconcile its findings against requirements only after it returns. If `code-review-blind` is unavailable, mark blind coverage unchecked; a general worker whose standing instructions require reading selected work documents is not a valid fallback.

## 4. Run one whole-change simplicity worker per round

Run one `code-review-simplicity` worker in each round of every full review, including a quick full-dimension review. Exclude it from an explicitly narrowed review unless the user explicitly includes it. Launch it alongside the other roles after the shared scope/requirements packet is ready.

Give it the pinned target, confirmed Work-ID and selected requirements/design context, explicit user decisions, scope/non-goals, relevant business/domain harms and the dedicated simplicity return contract. It asks whether optional capability/variation/generality can be removed or deferred, or an existing proven approach can eliminate a substantial new subsystem, while preserving confirmed requirements and safety. It reviews the whole change, not line-level style, internal ownership/lifecycle redesign or same-scope redesign, and proposes checks without executing shared validation.

Requirement-preserving simplicity proposals are candidates, not findings or votes. Tag them `R<n> simplicity`, verify the requirement and code evidence once, check user/business cost and strongest counterevidence, then classify only supported actionable proposals through the normal severity/gate rules. A proposal contradicting a confirmed requirement is an `optional scope challenge`: report it under `## Challenges`, never as a finding or readiness input. `No significant simplicity cut` completes the sample without inventing a finding. If `code-review-simplicity` is unavailable, use `general` with the same focused packet and explicit instruction not to perform the four dimension passes.

## 5. Run one approach worker per round

Run one `code-review-approach` worker in each round of every full review, including a quick full-dimension review. Exclude it from an explicitly narrowed review unless the user explicitly includes it.

Give it the same packet as simplicity, plus recorded design decisions/ADRs with their rationale and the analogous implementations collected in the history pass. It keeps the confirmed scope fixed, evaluates at least two credible alternative designs, and returns the alternatives it considered plus at most three proposals with improved axes, costs, evidence and the decision the user must make. It does not propose scope cuts (simplicity), internal ownership/lifecycle redesign (code health) or line-level defects (dimensions).

Approach proposals are challenges for user decision. Report verified proposals under `## Challenges`; they never change severity, blocking status or the verdict. When a proposal shows that the current approach causes a concrete reachable defect, validate that defect through the normal synthesis procedure and report it as a finding; the alternative remains a challenge. `Current approach is sound.` with the considered list completes the sample. If `code-review-approach` is unavailable, use `general` with the same focused packet and explicit instruction not to perform the four dimension passes.

## 6. Run one spec worker per round when requirements exist

Run one `code-review-spec` worker in each round of every full review, including a quick full-dimension review, when section 2 of the skill recorded at least one requirements source beyond the bare review request: a confirmed spec or plan, a linked ticket/issue/PRD, a PR description or discussion with requirements or acceptance criteria, or explicit user requirements/decisions. Otherwise record `spec: n/a - no requirements source` and launch none; do not ask the user only to enable this role. Requirement-source selection itself still follows the skill's work-identification and clarification rules. Exclude it from an explicitly narrowed review unless the user explicitly includes it.

Give it the pinned target, confirmed Work-ID, every recorded requirement source with locators, glossary/ADRs and relevant docs/contracts. It questions the requirements themselves: contradictions, wrong assumptions about the system, untestable criteria, missing cases, harmful requirements and inconsistent terms. It does not review code conformance; behavior workers do.

Route each verified concern by its class:

- `verification gap`: apply the skill's existing requirement-gap rule (targeted question or recorded gap with affected verification incomplete). List it under Coverage gaps, not Challenges.
- `soundness question`: report under `## Challenges`; it never changes severity, blocking status or the verdict.
- `spec-origin defect`: validate the concrete reachable harm through the normal synthesis procedure and report it as a finding labeled `spec-origin`; the fix may be a spec change. Also list the spec decision under `## Challenges`.

`No spec concerns.` with the sources checked completes the sample. If `code-review-spec` is unavailable, use `general` with the same focused packet and explicit instruction not to perform the four dimension passes.

## 7. Handle failures without bias

A denied or failed sampled worker gets one permitted sequential fallback using the same round/role packet and the same round model. If workers fail because that round's model is unavailable (no access, unknown model or provider error), do not retry it. Ask whether to rerun that round on the current model or mark it unchecked. Never fall back to another model silently; record any switch in the round-models line. A missing dimension specialist falls back to `general`. A failed simplicity, approach or spec worker gets one `general` fallback with its focused packet. Do not use `general` for the blind role, retry through broader permissions or tell another sample what the failed worker found.

If fallback cannot complete, mark that round/role coverage `unchecked` with the reason and next action. A failed sample is not a clean vote and cannot disappear because another round completed. Required unchecked coverage for any applicable role prevents `READY` unless the user explicitly narrowed it out before dispatch.

## 8. Build and verify the claim ledger

After every worker returns:

1. Record each candidate with source tags such as `R1 behavior`, `R2 code health`, `R1 blind`, `R2 simplicity`, `R1 approach` or `R2 spec`.
2. Merge only findings with the same trigger, failed behavior, root cause and remedy. Preserve distinct failures at the same location. Merge challenges only when they propose the same alternative or question the same requirement for the same reason.
3. Record support by distinct round: `found by 1/2 rounds` or `found by 2/2 rounds`. Multiple intent-aware dimensions in one round still count as one supporting round. When rounds used different models, name the models that found it, for example `found by 2/2 rounds (2 models)`; model diversity is attribution only, like agreement. Record blind support separately as `blind x/N` and challenge recurrence as `raised by x/N rounds`; neither counts as round agreement.
4. Treat agreement only as a confidence/tie-breaking signal. It is not evidence, does not establish correctness and never raises severity or promotes a challenge.
5. Validate every unique candidate once through the normal synthesis procedure: inspect the full path, strongest counterevidence, requirements and safe checks. Drop disproven candidates and unsupported challenges; retain consequential uncertainty as a gap.
6. Preserve every supported actionable finding and every supported challenge. No vote threshold and no top-N cap across rounds.

Report round completion per role, blind/simplicity/approach/spec coverage and worker failures. Perform static checks, final scope/worktree stability checks, artifact persistence and readiness synthesis once against the pinned target.

For follow-up reviews, the coordinator verifies the repair-closure ledger across affected code, callers, tests, docs/PR claims and newly applicable rules before the verdict. Gather prior findings and earlier challenge decisions once as shared historical evidence for intent-aware workers, never as another current sample's output; keep all such findings, decisions and rationale withheld from blind workers. Do not re-raise a challenge the user already decided unless new evidence changes it. Preserve unresolved obligations and distinguish old misses from later repair-induced issues rather than carrying an earlier clean verdict forward.
