# Work artifacts

Conventions shared by the skills in this repository for generated working documents: specs, plans, tickets, notes, reviews, glossaries and decisions.

## Work area

Artifacts live outside the repository, in one work area per repository shared by all of its worktrees, so removing a worktree never deletes them:

```text
<work-area> = ~/.agent-work/<repo-key>/
```

Resolve `<repo-key>` from any worktree:

1. Run `git rev-parse --path-format=absolute --git-common-dir`. Every worktree of a repository returns the same shared git directory.
2. If its name is `.git` or `.bare`, use the parent directory's name; otherwise use its own name without a trailing `.git`.

| Shared git directory | `<repo-key>` |
| --- | --- |
| `~/Developer/agents/.git` (normal clone) | `agents` |
| `~/Developer/acme-shop` (bare repo, worktrees inside) | `acme-shop` |
| `~/src/foo.git` (bare) | `foo` |
| `~/src/foo/.bare` | `foo` |

`<work-area>/.repo` holds the absolute shared git directory path. Write it on first use; if it names a different repository, stop and ask for a distinct key instead of mixing two repositories. Expand `~` to the absolute home path when a file tool does not. Outside a Git repository there is no work area; ask before writing artifacts.

All paths below are relative to `<work-area>`, not the current worktree, this repo or an installed skill directory:

```text
<work-area>/
  .repo                           # shared git directory of the owning repository
  work/<work-id>/
    spec.md                       # what and why; acceptance criteria
    plan.md                       # how; design, constraints, validation
    notes.md                      # grill-with-docs interview recovery notes
    tickets/index.md              # breakdown outline, statuses, coverage
    tickets/NN-<slug>.md          # one reviewed ticket per file
    reviews/                      # code-review / review-triage artifacts
  context/CONTEXT.md              # shared domain glossary
  context/CONTEXT-MAP.md          # optional multi-context map
  context/<context>/CONTEXT.md    # optional per-context glossary
  decisions/NNNN-<decision>.md    # approved architecture decisions
```

Use a stable kebab-case `<work-id>` matching the documents' Work-ID. Keep each work item's spec and plan together; shared domain context and ADRs stay outside individual work directories. Default to one `spec.md` and one `plan.md`. Only when explicitly needed and approved, use `specs/` and/or `plans/` within that work directory for multiple documents, with actual relative links. Do not reorganize existing files automatically.

Create lazily, only as needed. The work area is outside every worktree, so artifacts never appear in `git status` and need no ignore rules. Legacy in-repo `.agent-work/` folders remain covered by the managed global excludes file (dotfiles `gitconfig/dot-config/git/ignore`, stowed to `~/.config/git/ignore`); if legacy, tracked, or force-added `.agent-work/` content is staged, stop and ask without silently unstaging. Avoid secrets and customer data.

This convention governs generated working documents, not application source, tests, user-requested project documentation, or skill implementation files. Existing project docs remain useful evidence. Do not migrate earlier flat work-area layouts, legacy in-repo `.agent-work/` folders, `.prd/`, `docs/design/`, project glossaries or ADRs, or overwrite existing files automatically. Confirm legacy document selection and any migration first; preserve inbound links when moving an approved artifact.

## Commands

| Skill | Purpose | Output |
| --- | --- | --- |
| `create-plan` | Research and agree technical design | `<work-area>/work/<work-id>/plan.md` |
| `to-feature-spec` (formerly `to-prd`) | Capture agreed requirements, not a new interview | `<work-area>/work/<work-id>/spec.md` |
| `feature-spec-breakdown` (formerly `feature-spec-to-todos`) | Agree slice list, review each ticket, then optionally create todos or publish to a named tracker | `<work-area>/work/<work-id>/tickets/`; todos with `spec:<Work-ID>` prefix |
| `grill-with-docs` | Challenge design, settle terms, offer significant ADRs | `<work-area>/work/<work-id>/notes.md`, `<work-area>/context/` and `decisions/` |

Plan -> spec -> tickets is optional. A spec can precede its plan; simple work can have neither. Planning, document selection, and design approval never imply implementation approval.

## Spec <-> plan navigation

Every spec and plan has a stable `Work-ID`, explicit `Status`, and `Spec` / `Plan` fields. Use relative Markdown links, including a self-link. Example spec `<work-area>/work/session-restore/spec.md`:

```markdown
# Session restore — Feature Spec

**Work-ID:** session-restore
**Status:** Draft
**Spec:** [Session restore](./spec.md)
**Plan:** [Session restore plan](./plan.md)
```

Matching plan `<work-area>/work/session-restore/plan.md`:

```markdown
# Session restore — Design Doc

**Work-ID:** session-restore
**Status:** Draft
**Spec:** [Session restore spec](./spec.md)
**Plan:** [Session restore plan](./plan.md)
```

Use `Not created` for an absent counterpart, not a nonexistent file link. When the counterpart is created, reuse the confirmed work directory, update both headers through normal permissions and verify link targets, Work-ID matching the directory, and reciprocal links. Matching filenames/IDs or directory proximity alone do not establish selection. Multiple specs/plans require explicit user-confirmed relationships and lists of links rather than overwriting an existing pairing. If either write is blocked, report incomplete linkage. Read-only/draft workflows do not update either file.

ADRs include confirmed Work-ID and relative Spec/Plan links (for example `../work/session-restore/spec.md` and `../work/session-restore/plan.md` from `decisions/`), or absent markers for standalone decisions. Tickets link the actual source spec and plan (or `Not created`); never invent a local source file for pasted text. Decomposition leaves parent documents unchanged. Todo persistence is limited to what the available runtime guarantees; specs, plans and ticket files remain the cross-session source of truth.

## Session-start and handoff rule

Before code generation, implementation, review, or artifact editing:

1. Resolve `<work-area>` and inspect `<work-area>/work/` explicitly, even when normal search ignores hidden files. Identify candidate work directories and their specs/plans without loading every unrelated document. Follow explicitly selected legacy paths without silently migrating them.
2. An explicit user path, current-session confirmation, or validated reciprocal link from an already-selected document establishes identity. Otherwise ask the user to select. Offer likely candidates with path, title, status and short scope summary, plus **Other** and **None / standalone work**. Ask even when there is only one candidate. Do not infer selection from branch, filename, slug, recency, or unavailable prior-session memory. A clear new standalone request or no artifacts plus explicit ordinary task intent does not require creating documents.
3. Ask through the runtime's structured question interface when available; if no way to obtain an answer exists, return the blocker rather than guess. Example: "Which work describes this implementation: A, B, another path, or neither?" Preselection is only a recommendation awaiting confirmation.
4. Read the selected spec and plan, status, acceptance criteria, non-goals, design/testing choices, and relevant glossary/ADRs. Broken/one-way links, conflicting IDs, superseded docs or contradictory requirements require clarification. Do not quietly pair documents, choose the newer text, or mark Draft as approved.
5. Pass exact selected paths, Work-ID, status, relevant decisions and authorized scope to workers, or explicitly confirmed no-artifact context. A worker missing this identity must return candidate paths and a clarification request to the coordinator, not choose independently or launch new interviews it cannot complete.
6. Selection is context only. Respect each skill's implementation, review-item, write and publication gates. Report selected paths and any remaining ambiguity at handoff.

Each agent runtime's always-loaded global instructions should carry a short version of this rule; portable skills and isolated agent definitions also carry the relevant contract so it does not depend on this document being loaded.

## Maintenance acceptance checks

Static desk checks, not claims of observed agent behavior:

- New spec without plan -> `Not created`, no invented design or required scaffolding.
- Plan first, spec later -> reuse confirmed work directory and Work-ID; verify `./spec.md` <-> `./plan.md` links.
- Same-folder documents without confirmed current-work selection -> ask; proximity is not authorization.
- Fresh execution session with one plausible spec -> ask; do not auto-select.
- Several candidates / mismatched or broken links -> ask before acting on requirements.
- Explicit spec with valid reciprocal plan link -> read both without redundant identity interview.
- Read-only request / denied backlink write -> no silent mutation; report draft/incomplete pairing.
- Grill with existing `docs/adr/` -> read existing evidence; new ADR stays under `<work-area>/decisions/`.
- Two worktrees of one repository -> both resolve the same `<work-area>`; removing either worktree leaves artifacts intact.
- `<work-area>/.repo` names another repository -> stop and ask for a distinct key.
- Review/breakdown -> consume chosen context, preserve parent docs and existing approval gates; publish only accepted tickets on explicit instruction.
- Commit request -> work area is outside the repository; inspect the whole index for tracked or force-added legacy `.agent-work/` content.

Skill validation uses the externally installed `skill-writer` skill's checks; do not install its dependencies without approval. Runtime adherence needs separate model-session testing.
