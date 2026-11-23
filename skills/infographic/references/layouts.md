# Layouts

Pick one pattern. The layout is part of the lesson: a fix reads as before/after, a mechanism as a lifecycle, a design choice as a model.

## Choose

| Source signal | Pattern |
|---|---|
| Fixes a bug, replaces behavior, removes a pain | Before / after |
| Adds a mechanism, job, state machine or process | Lifecycle + three columns |
| Summarizes a feature spec or plan | Feature overview |
| Data model, schema, class or architecture choice | Model side by side |
| Recaps a session or a sequence of work | Session recap |
| Behavior over time, slots or a grid of cases | Grid before / after (variant of before / after) |

Two patterns fit: pick the one whose first glance shows the lesson. Still unsure: before / after for changes, overview for specs.

## Before / after

```text
[ BEFORE <claim>              ] | [ AFTER <claim>               ]
[ red pill: the problem       ] | [ green pill: the change       ]
[ scene: drawn objects, arrows] | [ same scene, fixed            ]
[ outcome card (e.g. history) ] | [ same card, now correct       ]
[ bold red caption            ] | [ bold green caption           ]
---------------- footer: limits or facts, one line ----------------
```

- Both halves use the same structure and positions so the eye compares them.
- Left warm tint, right cool tint, dashed divider with a small arrow circle.
- Scenes are objects (app window, envelope, file, database, person, calendar rows), not paragraphs.
- Grid variant: rows x columns of cells (booked / free, pass / fail), then a verdict badge per side ("AVAILABLE" vs "UNAVAILABLE").

## Lifecycle + three columns

```text
                 Title
A <THING>'S LIFE  (state) -> (state) -> (state) -> 2-3 outcome pills
WHERE IT BROKE | WHAT WE ADDED (numbered) | WHAT USERS SEE
[problem cards]| [1. ...] [2. ...] [3. ...] | [table or mock UI]
[side note]    |                            | [non-goal / trade-off]
              footer: one-line takeaway
```

- The state strip is pills with arrows; branch the final state into outcome pills when there are several.
- The middle column is numbered steps; each has a bold line and at most two short sub-lines.
- The right column shows the user-visible result with real-looking rows.

## Feature overview

```text
                 Title / subtitle
A <THING>'S LIFE  pills with arrows (+ small red branch for expiry or failure)
WHERE YOU ...   | HOW IT WORKS (mini diagram) | GUARDRAILS (4-5 slim rows)
[2 cards]       | [boxes + links + caption]  | [icon + bold line + sub-line]
[example card: history entry, API call or screen mock] [secondary card]
              footer: one-line takeaway
```

- Use for a spec or plan with several facets. Keep each card to a title, a description and chips or bullets.

## Model side by side

```text
   <Option or part A>          |      <Option or part B>
 [table: name + field pills]   |  [table] --1-to-1-- [table]
 [subtypes] -> inherits        |
          caption: when to use which, one line
```

- Tables have a header band and fields as small pills; mark new or special fields with an accent fill.
- Relationship labels on the links ("1-to-1", "inherits", "has many").

## Session recap

```text
                 Title: the session goal
 GOAL -> (step) -> (decision, check icon) -> (step) -> OUTCOME
 DECIDED [3-5 check rows] | CHANGED [files or areas as chips] | OPEN [2-3 items]
              footer: one-line takeaway
```

- Only what happened in the session. Decisions get checks; open items get a neutral circle, not red.

## Budgets

| Element | Limit |
|---|---|
| Strings in the whole image | about 40 |
| Zones | 2 halves or 3 columns, plus at most one bottom row |
| Cards per column | 2 large or 5 slim |
| Words per label | 6 |
| Characters per line | 45 |
| Bullets per card | 3 |

Over budget: cut to the lesson, then offer a second image.
