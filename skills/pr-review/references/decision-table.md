# Decision table

Open by default after building the shortlist, unless the user asked for one by one. It uses the same bucketed table as `review-triage`'s Table mode, with outgoing actions. Evidence, drafting, event, exact-preview and publication rules from `SKILL.md` still apply. The table never publishes.

## 1. Verify the whole shortlist first

- Before asking anything, verify every item with the section 2 evidence rules, in source order. Check trigger, impact, reachability (UI, API or crafted request) and counterevidence, independent of the report's conclusion. P-labels, round votes and reviewer confidence never shorten verification.
- Workers may check items in parallel:
  - **Batch:** group items by file or area, about 5 per worker, with at most about 6 workers running at once.
  - **Input:** pinned PR/head SHA, each item's `review.md` source range and the section 2 rules.
  - **Output per item:** verdict, reachability, impact, decisive `path:line` evidence, unknowns and a draft comment.
  - **Access:** read-only. Workers read code, search and read history. They never write files, run probes, check out branches or touch the PR.
  - **Failure:** if a worker crashes, times out, skips an item, or returns a verdict without `path:line` evidence, the item goes to C as `worker failed: <reason>`.
  - **Re-check:** before placing an item in A or B, open its cited `path:line` and confirm it supports the verdict. Otherwise the item goes to C.
- Keep `covered by #M` links.
- Draft each bucket A comment with section 3 style.
- Append one dense line per item to `feedback.md`: `- <UTC> #N bucket A|B|C; rec: Keep|Omit|Investigate; evidence: <path:line>; unknowns: <...>`.

## 2. Buckets

| Bucket | Put an item here when | Recommendation |
| --- | --- | --- |
| **A - Keep, sure** | A verified introduced or worsened defect with real impact, a broken contract or substantial maintenance cost. The wording needs no further decision. Also a supported challenge or a gap the author must answer, drafted as a question | Keep |
| **B - Omit, sure** | Taste or cleanup nits, feedback already in a thread, disproven claims, unrelated pre-existing problems, gaps and requirements the author need not act on, out-of-touch observations, harmless misuse or very rare harmless cases under fail first (never security) | Omit |
| **C - Your call** | Incomplete evidence, disputed reachability, unknown frequency on a serious claim, weight or tone questions (blocking or not), and anything needing Investigate | Item's own actions, recommendation first |

When a choice between buckets is unclear, or fail first may apply but harmlessness, documentation or reachability is uncertain, use C so the user checks. An omission never resolves a serious risk; it still constrains the event recommendation.

## 3. Present one table, ask once

Persist the table in `feedback.md`, then ask one self-contained question containing it:

```markdown
### PR feedback table - <total> items: A <n> keep, B <n> omit, C <n> your call

**A - Keep, sure**
- #2 P1 `api/orders.rb:88` - Refund skips tenant check - "Any user can refund another tenant's order through the API, since..."
- ...

**B - Omit, sure**
- #6 P3 `ui/list.tsx:14` - Rename variable - Omit: taste
- ...

**C - Your call**
- #9 P2 `jobs/sync.rb:30` - Possible double sync - rec: Investigate
  Two workers can pick the same row (`jobs/sync.rb:30`). Whether a lock exists upstream is unverified.
- ...

Reply: `go A B` · `walk C` / `walk 4 9` · `explain 9` · `9 keep` · `4 omit` · `2 reword: shorter, drop the example`
```

- Each A row shows the first sentence of its draft. Each B row is one line. Each C row adds at most two short sentences. When C has more than 15 rows, show 10 per page.
- Options, recommendation first: **Apply A + B, walk C**, **Apply A + B, omit C**, **Walk everything** (Step mode for all items). A custom answer takes the reply commands.
- Log the exact reply as one decision event per named item. Unnamed items stay **pending** and are never published or silently omitted. If part of the reply is ambiguous, log Investigate for only the affected items and ask about that part.
- `explain N` shows item N's full Step card (assessment plus complete draft) with its actions plus **Back to table**. `reopen N` moves an item back to C as pending.
- Keep still means "include this wording", not "publish".

## 4. After decisions

1. Apply Reword requests. Then walk the named items Step-style, with no continuation stops between them.
2. Before the event step, check the head SHA and discussion again. A changed head or new thread can move an item back to C.
3. When the walk finishes, report `#N | Keep/Omit/pending | note` and ask about pending items: **Walk them**, **Omit all** or **Leave pending**.
4. Continue with `SKILL.md` section 4. The event recommendation, the exact full preview and the explicit publication authorization are always separate questions.

## Examples

- **Happy path:** 12 items. The table has A 2, B 9, C 1. The user replies `go A B, walk C`. Item #9 gets Investigate, then Omit. Event COMMENT, preview, authorization, then publish.
- **Robust variant:** after the table, the head moves and #2's file changes. #2 goes back to C and is re-verified before the preview.
- **Anti-pattern:** a serious-sounding race ("this could double-charge") is put in A with no evidence of concurrent callers. **Correct:** a serious claim with unverified reachability goes in C with its settling check, or is drafted as an explicitly uncertain question only after the user chooses.
