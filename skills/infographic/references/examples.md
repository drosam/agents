# Examples

All examples are invented.

## Happy path: PR to before / after

Source: a PR titled "Webhooks: retry failed deliveries with backoff". Body: failed deliveries were dropped after one try; now they retry 5 times (1 min, 5 min, 30 min, 2 h, 12 h), then the endpoint is marked failing and the admin gets an email. The delivery log shows each attempt.

Content sheet:

```text
Lesson:   A failed webhook is retried five times instead of lost.
Layout:   Before / after - the PR replaces "drop after one try".
Title:    "Webhook retries"
Zones:    BEFORE "one try, then gone": red pill "A failed delivery is lost";
            app server -> red X on arrow -> partner server labeled "Partner endpoint";
            delivery log card "Delivery log": row "order.created · 500 · dropped".
          AFTER "five tries with backoff": green pill "Retried until it lands";
            timeline of 5 dots "1 min", "5 min", "30 min", "2 h", "12 h", last dot green;
            delivery log card: rows "attempt 1 · 500", "attempt 2 · 500", "attempt 3 · 200 delivered".
Example:  order.created event, HTTP 500 then 200.
Takeaway: "After 5 failures the endpoint is marked failing and the admin is emailed"
Cut:      Backoff jitter and queue internals (not visible to users).
```

Brief excerpt (AFTER half):

```text
RIGHT HALF, top: bold heading "AFTER" followed in lighter weight by "five tries with backoff". Under it a soft green pill: "Retried until it lands".
  - A horizontal timeline of five dots connected by a thin line, labeled under each dot: "1 min", "5 min", "30 min", "2 h", "12 h". The first two dots are red, the third is green with a check.
  - A delivery log card headed "Delivery log" with three rows: "attempt 1 · 500", "attempt 2 · 500", "attempt 3 · 200 delivered" (the last row highlighted green).
```

## Robust variant: session recap with sensitive data and too much content

Source: the current session debugged a failed import for a customer and changed four things.

- The session showed a real customer email, an API token in a curl command, and an internal hostname. The sheet uses `jane@example.com` and "Customer A", drops the token, and writes the host as "import worker". The report lists these placeholders.
- The session covered the bug, a refactor and two unrelated config tweaks. Lesson: "Imports failed because dates were parsed in the server's time zone." The sheet keeps the bug and its fix; the refactor and tweaks go in "Cut", and the report offers a second image for them.

## Anti-pattern and correction

Bad brief:

```text
Make an infographic summarizing the plan in work/webhooks/plan.md. Include all the user stories from the spec and the decisions from ADR 0004. Use our usual style.
```

Problems: the model cannot read local files, the ADR or "our usual style"; "all the user stories" blows the text budget; no layout, strings or objects are given.

Corrected opening:

```text
Create a 16:9 landscape before/after illustration for a pull request description. It should explain webhook retries mostly through pictures, with very little text. The result should look like a clean editorial tech illustration, ready to publish.

STYLE: clean flat vector illustration with soft shading, friendly rounded shapes, thin outlines, gentle drop shadows. Left half warm beige (#F7F4EF), right half cool light gray-blue (#F1F5F9), separated by a thin dashed line with a small white circle holding a right arrow. Red for problems, green for the fix, blue for servers. Geometric sans-serif (Inter-like), dark navy text. Large, readable, few words.

TITLE (top center, large bold): "Webhook retries"
...
```
