# Agents

Shared agent skills and sub-agent definitions.

## Layout

- `skills/` - [Agent Skills](https://agentskills.io/specification), one directory per skill with a `SKILL.md`.
- `agents/` - sub-agent definitions (Markdown with frontmatter).

## Workflow

How the skills and agents chain together. Define is optional; simple work starts at Build. Every arrow crossing a gate needs explicit user approval. Artifact layout, spec/plan linking and session-start rules: [`docs/work-artifacts.md`](docs/work-artifacts.md).

```mermaid
flowchart TD
    subgraph S0["0 Session start"]
        rules["Agent instructions<br/>permission policy"]
        gate{"Artifact gate<br/>user selects .agent-work spec/plan?<br/>ask, never guess"}
        rules --> gate
    end

    subgraph S1["1 Define (optional, any order)"]
        grill["grill-with-docs (grill me)<br/>work/&lt;id&gt;/notes.md<br/>context/CONTEXT.md<br/>decisions/NNNN.md"]
        plan["create-plan<br/>work/&lt;id&gt;/plan.md"]
        spec["to-feature-spec<br/>work/&lt;id&gt;/spec.md"]
        breakdown["feature-spec-breakdown<br/>tickets/NN-*.md<br/>optional todos / tracker"]
        grill <--> plan
        plan <-->|reciprocal links| spec
        spec --> breakdown
        plan --> breakdown
    end

    approve{{"Design approved != implementation approved"}}

    subgraph S2["2 Build"]
        tdd["tdd (external)<br/>red-green-refactor"]
        debug["debug / prod-debug<br/>read-only diagnosis"]
    end

    subgraph S3["3 Verify"]
        review["code-review"]
        workers["workers: behavior, blind,<br/>code-health, security,<br/>simplicity, tests"]
        simplify["simplify-code<br/>propose, edit approved only"]
        qa["qa-review<br/>Playwright + Figma"]
        review --> workers
    end

    subgraph S4["4 Feedback"]
        triage["review-triage (all incoming feedback)<br/>one item at a time"]
        sources["Feedback sources<br/>code-review, simplify-code, qa-review,<br/>GitHub / GitLab / other PR/MR comments,<br/>human reviewers, pasted bug lists"]
        sources --> triage
        prr["pr-review (outgoing)<br/>publish only after exact preview approved"]
    end

    subgraph S5["5 Ship"]
        commit["commit<br/>focused commits<br/>never stage .agent-work/"]
    end

    subgraph META["Side lane: meta"]
        meta["skill-writer, find-skills (external)"]
    end

    gate -->|new or selected work| S1
    gate -->|standalone task| S2
    breakdown --> approve --> S2
    debug --> tdd
    S2 --> S3
    S3 -->|findings| sources
    triage -->|Fix: one commit per fix| commit
    S3 -->|clean| commit
    commit -.->|next ticket| S2
```

## Install

Installed by the dotfiles installer (`install-dotfiles`), which clones this repository to `~/Developer/agents` and links it into `~/.agents`:

```bash
mkdir -p ~/.agents/skills
stow -d ~/Developer -t ~/.agents agents
```

`~/.agents/skills` stays a real directory so skills installed with `npx skills` live beside the linked ones without landing in this repository.

### External skills

The workflow also uses these upstream skills, installed separately with `npx skills` and not kept in this repository:

| Skill | Source | License |
| --- | --- | --- |
| tdd | [mattpocock/skills](https://github.com/mattpocock/skills) | MIT |
| find-skills | [vercel-labs/skills](https://github.com/vercel-labs/skills) | MIT |
| skill-writer | [getsentry/skills](https://github.com/getsentry/skills) | Apache-2.0 |

Install them globally for Pi (`~/.agents/skills`) and Claude Code (`~/.claude/skills`). Requires Node.js 22.20 or later.

1. Install the skills:

   ```bash
   npx skills add mattpocock/skills --skill tdd -g -a pi -a claude-code
   npx skills add vercel-labs/skills --skill find-skills -g -a pi -a claude-code
   npx skills add getsentry/skills --skill skill-writer -g -a pi -a claude-code
   ```

2. Check them with `npx skills ls -g`, and update later with `npx skills update -g`.

Restart running agent sessions to pick up the new skills.

## Upstream sources

Each skill's `SOURCES.md` records full provenance, decisions and validation. "Based on" means the local skill adapts that upstream skill; "Pattern reference" means ideas were compared but the skill is a local synthesis. Revisions are the ones last inspected.

| Skill | Based on | Pattern reference |
| --- | --- | --- |
| code-review | Local | Google eng-practices; OWASP |
| commit | Local | [getsentry/skills](https://github.com/getsentry/skills/tree/c2f99a5b04b4cd992ec3022d7c2c3e23e938d241) `commit` |
| create-plan | Local | [getsentry/skills](https://github.com/getsentry/skills/tree/c2f99a5b04b4cd992ec3022d7c2c3e23e938d241) `skill-writer` |
| debug | Local | - |
| feature-spec-breakdown | [mattpocock/skills](https://github.com/mattpocock/skills/tree/9e2abf8611a345efbf779aacb171cff015bcdeb6) `to-tickets` | - |
| grill-with-docs | [mattpocock/skills](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7) `grill-with-docs`, `grilling`, `domain-modeling` | - |
| pr-review | Local | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official); [feiskyer/claude-code-settings](https://github.com/feiskyer/claude-code-settings/tree/95dab59a62b2031adcb7abf25ae0a60b8a13fdb2) |
| prod-debug | Local | - |
| qa-review | Local | [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp); [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser/tree/39a74c70d7759d5a6de7a22c04570bb626bbd081); [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli/tree/b85c7a736bb473bf55b584e54a09ffa698d6d871) |
| review-triage | Local | [obra/superpowers](https://github.com/obra/superpowers/tree/5bf4e78011075bcfc0dc295f0724994cd123ee71) `receiving-code-review` |
| simplify-code | Local ([grugbrain.dev](https://grugbrain.dev/) philosophy) | [getsentry/skills](https://github.com/getsentry/skills/tree/c2f99a5b04b4cd992ec3022d7c2c3e23e938d241) `code-simplifier`; [anthropics/claude-code](https://github.com/anthropics/claude-code/tree/d78be9481b889e11186ec4578b4f5e9301396e25); [mattpocock/skills](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7) |
| to-feature-spec | [mattpocock/skills](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7) `to-spec` | - |

When refreshing a skill from upstream, keep local contracts (approval gates, work-artifact identity, title-only commits) over upstream defaults.

## License

[MIT](./LICENSE).
