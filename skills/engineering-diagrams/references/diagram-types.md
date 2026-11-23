# Diagram Types

Pick the type from the question the reader needs answered. If a markdown table or a five-line list says the same thing, write that instead of a diagram.

## Selection

| Reader question | Type | Typical source sections |
|---|---|---|
| What data exists and how is it linked? | Data model (ERD) | Plan data model, migrations, ADRs |
| Which path does the code take, and why? | Decision flow | Plan design steps, spec rules and edge cases |
| Who calls whom, in what order, with what result? | Sequence | Plan request flow, API section, spec user journey |
| What states can one record be in, and what moves it? | State / lifecycle | Plan lifecycle, cleanup and deletion rules, spec acceptance criteria |
| Which parts and boundaries does the change touch? | Component / context | Plan background and design overview |
| What is on or off under a flag, plan or role? | Table, not a diagram | Plan rollout or flag section |

One diagram answers one question. When a diagram needs two titles, split it.

## Budgets

| Type | Boxes | Edges | Other |
|---|---|---|---|
| Any | 9 target, 12 max | 12 target, 16 max | 2 notes, 2 focal elements, 1 grouping criterion |
| ERD | 8 entities | 1 per relationship | 8 fields per entity, then `+ N more` |
| Sequence | 5 lifelines (6 max) | 12 messages | 2 `alt`/`opt` frames, nesting depth 1 |
| State | 9 states | 10 transitions | 1 global `* -> X` note |

Over budget: split into an overview diagram plus detail diagrams, and cross-reference them in the subtitle ("detail of diagram 02").

## Data model (ERD)

- One box per table: header row with the table name (15px 600) and a tag (`NEW`, `EXISTING`, `JOIN`); body rows in 12px mono.
- Prefix keys: `# id` for the primary key, `-> email_id` for a foreign key. Put the type or constraint right-aligned in `#475569` when it matters (`unique`, `1 B - 5 MB`).
- Show only columns the design depends on. Existing tables list just the columns this work reads or adds.
- One relationship line per foreign key, drawn between the related tables. Always draw it the same way: from the table holding the FK to the table it references, arrowhead at the referenced table.
- Put cardinality on masked labels at both ends, 10-12px from the box: `1`, `N`, `0..1`. Label the line with a verb when it is not obvious (`links`, `uploaded by`).
- Constraints that do not fit a row (cascade rules, cleanup jobs, immutability) go in one note box, placed beside the tables it governs rather than between relationship lines.
- Storage outside the database (S3, blob store) uses the External role and a cylinder, joined to the column that stores its key.

## Decision flow

- Read top to bottom. Main path straight down the left or centre column; "no" or exception branches step right.
- Decisions: phrase as a yes/no question. Label every exit (`yes`, `no`, or the option name). At most 3 exits.
- Terminal outcomes are boxes with the outcome role: New for "files linked", Failure for "422", Existing for "no change".
- Entry points (callers) sit on the left or top, grouped by one criterion. If callers converge on one method, draw them into that method once.
- Show the order of checks explicitly; when order matters, number decisions (`1`, `2`, `3`) in the box.

## Sequence

- Lifelines left to right in first-call order; the human or initiating UI on the far left, external systems on the far right. Header boxes 52 high, lifelines dashed `3 3` `#cbd5e1`.
- Messages: solid line with filled head = call; dashed with filled head = return; solid with open head = async (enqueue, webhook). Every call is labeled; label returns only when the value matters later.
- Messages never point upward. Space them 28-36px apart; keep labels above the line.
- Branches use an `alt` frame (`data-role="frame"`, `rx=8`, fill `#f5f5f4`, 11px uppercase tab label) with each guard in brackets: `[fits]`, `[too large]`. Use `opt` for a single optional block and `loop` for polling.
- Phase bands (`1 UPLOAD`, `2 SEND`) are fine for long flows; label them with 11px uppercase headings, not color alone.
- Notes over a lifeline get `data-role="note"`. Outcome summaries go below the last message, after the lifelines end, never across them.
- Self-calls are short notes beside the lifeline ("sniff real type"), not loops.

## State / lifecycle

- States are rounded boxes named as conditions ("Linked to emails"), with the storage or code identifier as sublabel.
- Start dot top-left; final states bottom or right with the end ring, tagged `FINAL`.
- Transition labels read `event [guard] / action`, for example `cleanup job [unlinked > 14 days] / delete row + file`.
- Check for black holes (no exit, not final) and miracles (no entry, not start). Either fix them or add a note explaining why.
- States must be mutually exclusive. If a record can be in two at once (linked to a template and to emails), model the dimensions separately or use a decision flow instead.
- Lifecycle layout: main progression in the middle row, waiting or retry states above, terminal outcomes below.

## Component / context

- One zoom level per diagram: system context, containers or components; never mixed.
- Each box: name, a sublabel with its responsibility, and a tag for technology or status (`RAILS`, `SIDEKIQ`, `EXTERNAL`).
- Each line: one direction, a verb label, and the protocol on process boundaries (`HTTPS JSON`, `SQL`, `S3 API`).
- Group with frames by one criterion only (deployment unit, or team, or trust boundary).
