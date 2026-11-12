---
name: writing-for-humans
description: Writes and edits text that other people will read in collaboration tools (GitHub, GitLab, Linear, Jira, Slack, Teams and similar) so it is short, direct and sounds like a person, without dropping facts. Use when drafting, rewriting or posting PR/MR review comments and replies, PR/MR descriptions, issue, ticket or work-item bodies and comments, status updates, or chat messages, or when asked to make such text shorter, less wordy, less robotic or more human. Not for replies to the user in the current conversation, code comments, documentation files or commit messages.
---

# Writing for Humans

Write the way a busy, friendly senior engineer types: point first, plain words, nothing the reader already knows, nothing they need left out.

## Scope

- Apply only to the text being drafted for publication. The conversation with the user keeps its own style; switch back after the draft.
- Write full natural sentences in the draft even when the conversation uses a compressed or terse style. Fragments and shorthand read as robotic in public.
- This skill shapes wording only. It grants no permission to post; follow the caller's or user's approval rules.
- A repo, team or tracker template wins over the defaults below. Fill the template in this voice.

## Workflow

1. **Reader and action.** Name who reads it and what they must do: fix, answer, decide, review, or nothing. Note what they already know from the thread, ticket or PR.
2. **Point first.** The first sentence carries the ask, answer, decision or problem. No run-up.
3. **Keep the facts.** List what the reader needs to act and keep all of it: error text, values, versions, paths, links, repro steps, impact, who is affected, deadlines. Shorten wording, never data.
4. **Add only what helps.** One reason when the ask is not obvious. A short example, snippet or repro when it makes the problem faster to see. Bullets when there are 3+ parallel items (steps, criteria, options, affected cases).
5. **Cut.** Remove every tell in the cut list below.
6. **Check length.** Compare with the budget. Over budget: cut wording first; if every remaining line is a needed fact, keep it. Never compress into fragments to fit.
7. **Final check.** Run the pre-publish checklist.

## Length budgets

Defaults, not caps. Needed facts beat the budget; filler never does.

| Text | Default |
|------|---------|
| Inline review comment | 1-3 sentences, plus a snippet or `suggestion` block if it helps |
| Reply in a thread | 1-2 sentences; often one |
| PR/MR description | 1-3 sentence summary of what and why; short bullets for notable changes, testing and risks only when present |
| Bug report | Title + 1-2 sentence summary + steps, expected, actual, environment |
| Feature request / ticket | Title + problem and outcome in 1-3 sentences; acceptance criteria as bullets |
| Ticket comment / status update | 1-3 sentences: state, next step, blocker or ask |
| Chat message | 1-3 sentences in one message; thread long detail |

Ceiling: it fits on one screen, unless the content is itself a log, table or list the reader asked for.

## Voice

- Plain words and contractions (`it's`, `don't`, `I'd`). Talk about the code or the change, not the person.
- State what you know; ask when you are unsure. One hedge at most per claim.
- Mark weight when it matters: `nit:`, `optional:`, `non-blocking:`, `blocking:`. Use the team's label convention if it has one; do not introduce a new one.
- Match the thread's language, register and formatting. When recent comments from the same team are available, mirror their length and tone.
- Thanks or praise only when genuine and specific, once, briefly.
- Disagree calmly: the fact, the consequence, the proposal. No defensiveness, no apology chains.

## Cut list

| Tell | Looks like | Do instead |
|------|-----------|------------|
| Chat wrapper | "Great question!", "Happy to help", "I hope this helps", "Let me know if you have any questions" | Delete |
| Run-up | "I wanted to flag", "Here's the thing", "It's worth noting that", "Just a heads up" | State the point |
| Recap the reader has | Reply restates the problem and diagnosis before the answer | Answer first; keep only the fact they lack |
| Work narration | "I've carefully reviewed", "After analyzing the code", "I went ahead and" | Delete; give the result |
| Fake contrast | "This isn't just X, it's Y", "Not X, but Y" | Say Y |
| Inflated words | crucial, robust, comprehensive, seamless, leverage, ensure, enhance, delve, significant, key | Plain word or delete |
| Stacked hedges | "might potentially", "could possibly", "it seems like it may" | One hedge or none |
| Over-politeness | "Would you mind possibly considering" | "Could you...?" |
| Decoration | Headings or bold labels in short text, emojis, a bullet list for two items | Prose |
| Forced threes | "faster, safer, and more maintainable" when one is true | Keep only the real items |
| Dashes everywhere | em or en dashes joining clauses | Comma, period or parentheses, unless the user's own writing uses them |
| Summary closer | "Overall, this change improves...", "In summary" | Delete |
| Robot shorthand | "Null deref L42. Fix: early return." | Full short sentences |

## Formatting

- Use the target's syntax. When unsure, plain text with code spans.
- Code spans for identifiers, paths and values; fenced blocks for multi-line code or logs; trim logs to the relevant lines.
- Links instead of pasted long URLs. Refer to issues, commits and PRs with the platform's link form.
- No headings in comments or chat. In descriptions, use headings only when a template has them or the body has several distinct parts.

## Pre-publish checklist

- First sentence carries the point.
- Reader knows what to do, or that nothing is needed.
- Every fact, number, name, link and error from the source survived.
- Every sentence adds something the reader did not have.
- No cut-list tell remains.
- Within budget, or every extra line is a needed fact.
- No secrets, tokens, credentials, customer data or private URLs the audience should not see. Redact log and screenshot content.

## Examples

Review comment:

> Bad: Great work on this PR! I noticed a potential issue that might be worth considering. It seems that `fetchUser` could potentially return `null` in certain edge cases, which may lead to unexpected behavior. It would be beneficial to add a null check to ensure robustness. Let me know what you think!
>
> Good: `fetchUser` returns `null` when the session has expired, and line 42 reads `.id` from it. Could we return early here?

Reply after fixing:

> Bad: Thank you so much for catching this! You're absolutely right. I've gone ahead and updated the code to properly handle this case by adding validation.
>
> Good: Good catch, fixed in `a1b2c3d`.

More cases (PR description, bug report, ticket, status update, chat, disagreement, secrets, over-shortened text): read `references/examples.md` when drafting one of those types or when a draft still sounds robotic after the cut list.
