# Examples

## 1. Happy path: diagrams from a selected spec and plan

Imaginary work item: a pet clinic app adds appointment reminders by SMS and email.

Request: "Draw diagrams for the appointment-reminders plan."

1. Identity: the user named the work item; read `work/appointment-reminders/spec.md` and `plan.md`, which link to each other. Read the ADR the plan cites.
2. Brief shown to the user before drawing:

```text
Diagram set - appointment-reminders (spec Draft, plan Draft)
01 data-model (ERD) - "What tables does this add?" - plan 1, 2; ADR 0007
02 channel (decision flow) - "Does a reminder go by SMS, email or not at all?" - plan 3; spec AC-2, AC-3
03 send-flow (sequence) - "What happens from booking to delivery?" - plan 4, 5; spec AC-4
04 lifecycle (state) - "What states can one reminder be in?" - plan 2, 6
Opt-out rules per country -> markdown table in README, not a diagram (plan 7)
Open: spec says remind 24 h before, plan says 48 h. Which is right?
```

3. After the user answers and approves, draw each from `assets/skeleton.svg`, eyebrow `ERD · APPOINTMENT-REMINDERS · PLAN 1, 2`.
4. Run `scripts/check_svg.py` on all four, fix errors, render each, name at least one defect per diagram, fix and re-render.
5. Write `diagrams/README.md` with the source mapping, then propose this plan.md snippet without applying it:

```markdown
Diagrams: [data model](./diagrams/01-data-model.svg), [channel](./diagrams/02-channel.svg), ...
```

## 2. Robust variant: missing facts and conflicting sources

Request: "Add a sequence diagram for the retry flow" while the plan covers retries in one sentence and the code shows a different job name.

- Do not invent the missing steps. Draw what the plan states, put `?` on unknown messages ("retry backoff ?"), and list them under Open questions in the reply.
- Plan vs code mismatch (plan says `ReminderJob`, code has `NotificationJob` at `app/jobs/notification_job.rb:12`): ask which the diagram should show. Use the `EXISTING` tag for what code has today and `NEW` for what the plan adds.
- Spec vs plan conflict: stop and ask; never pick the newer document.
- No spec or plan, standalone request: draw from code and user input, set the eyebrow source to `STANDALONE`, cite file:line in the README sources column, and ask where to save when the user gave no path.
- Image viewing unavailable: run the checker, then report "visual check skipped" instead of claiming the diagram looks right.

## 3. Anti-pattern and correction

Before (one diagram, many problems):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 500">
  <!-- no title/desc/role; transparent background; no legend -->
  <rect x="40" y="40" width="160" height="50" rx="14" fill="#2dd4bf"/>
  <text x="50" y="70" font-size="16">ReminderService handles everything</text>
  <path d="M200 65 C 400 0, 500 300, 700 260" stroke="#2dd4bf" fill="none"/>
  <text x="380" y="150" font-size="9">maybe retries?</text>
</svg>
```

Problems: meaning carried by teal fill only; text overflows the box; curved connector crossing the canvas; 9px sentence-case label; "maybe retries?" is a guess not traced to the plan; invented service name; no accessible name; transparent background.

After:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 300" width="760" height="300" role="img"
     aria-labelledby="sched-title sched-desc" font-family="Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif">
  <title id="sched-title">Appointment reminders - scheduling</title>
  <desc id="sched-desc">Confirming an appointment slot schedules one reminder row for later delivery.</desc>
  <defs><marker id="sched-arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0 L10 4 L0 8 z" fill="#0f766e"/></marker></defs>
  <rect width="760" height="300" fill="#fafaf9"/>
  <text x="40" y="32" font-size="10" letter-spacing=".14em" fill="#64748b" font-family="ui-monospace, Menlo, monospace">FLOW · APPOINTMENT-REMINDERS · PLAN 2</text>
  <text x="40" y="62" font-size="28" fill="#0f172a" font-family="'Iowan Old Style', Georgia, serif">Reminder scheduling</text>
  <path d="M280 152 H478" stroke="#0f766e" stroke-width="1.5" fill="none" marker-end="url(#sched-arr)"/>
  <rect x="330" y="132" width="100" height="16" fill="#fafaf9"/>
  <text x="380" y="144" font-size="12" fill="#0f172a" text-anchor="middle">slot confirmed</text>
  <rect x="60" y="120" width="220" height="64" rx="6" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
  <text x="76" y="148" font-size="15" font-weight="600" fill="#0f172a">POST /appointments</text>
  <text x="76" y="168" font-size="12" fill="#475569">clinic API</text>
  <rect x="480" y="120" width="220" height="64" rx="6" fill="#f0fdfa" stroke="#0f766e" stroke-width="1.5"/>
  <text x="496" y="148" font-size="15" font-weight="600" fill="#0f172a">Reminder scheduled</text>
  <text x="496" y="168" font-size="11" fill="#475569" font-family="ui-monospace, Menlo, monospace">reminders</text>
  <rect x="648" y="128" width="44" height="16" rx="2" fill="#ffffff" stroke="#0f766e"/>
  <text x="670" y="140" font-size="9" font-weight="700" letter-spacing=".06em" fill="#0f766e" text-anchor="middle">NEW</text>
  <g id="legend">
    <line x1="40" y1="246" x2="720" y2="246" stroke="#e7e5e4"/>
    <rect x="40" y="262" width="16" height="16" rx="3" fill="#f0fdfa" stroke="#0f766e" stroke-width="1.5"/>
    <text x="64" y="275" font-size="12" fill="#334155">New (also tagged NEW)</text>
    <rect x="220" y="262" width="16" height="16" rx="3" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
    <text x="244" y="275" font-size="12" fill="#334155">Existing</text>
  </g>
</svg>
```

What changed: names come from plan section 2; status is shown by both fill and tag; the connector is straight and labeled on a mask; text fits with 16px padding; accessible name, opaque background and legend are present.
