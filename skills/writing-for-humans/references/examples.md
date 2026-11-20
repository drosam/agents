# Examples

Synthetic before/after pairs. Each "Good" keeps every fact from "Bad" that the reader needs.

## Contents

- Review batch with summary body
- PR/MR description
- Bug report
- Ticket with acceptance criteria
- Status update
- Chat message
- Disagreeing in a thread
- Unsure claim
- Secrets and customer data
- Anti-pattern: shortened by dropping facts
- Anti-pattern: robot shorthand

## Review batch with summary body

Adapted from real agent drafts that were correct but read as robotic; identifiers changed.

Bad:

> Body: Looks good. The inline notes are all non-blocking.
>
> 1. non-blocking: the reports page used to sort labels case-insensitively, but `LabelFilter` uses a plain `sortBy`, so `Zebra` now shows before `apple` here. If the old order matters, sorting by `name.toLowerCase()` in `LabelFilter` would fix it, though that also reorders the other screens.
> 2. non-blocking: clearing the last label now sends `labels: undefined` instead of `[]`, and `handleFilter` drops undefined keys before tracking, so "Filtered orders" no longer fires for it. Probably fine, but worth a quick check if anyone relies on that event.
> 3. Until the projects load, every saved pick shows as "Deleted project", since `projects` starts as `[]`. If the request fails, `.catch(() => [])` makes that stick, so someone could remove picks that still exist. Could we only label ids as deleted after a successful load, like `ProductConditionForm` does with `savedLoaded`? Not blocking.
> 4. Small one: this line still says thirty-five condition types and "covers all thirty-five", and the list doesn't include Projects. Should be thirty-six, with Projects after Products.

Good:

> Body: Looks good! A few small things below, feel free to skip any you disagree with.
>
> 1. Should labels still ignore case here? `Zebra` now sorts before `apple` because `LabelFilter` uses a plain `sortBy`. Sorting by `name.toLowerCase()` there would change the other screens too.
> 2. Clearing the last label no longer fires "Filtered orders", since it now sends `undefined` and `handleFilter` skips undefined keys. Does anything depend on that event?
> 3. Saved picks show as "Deleted project" until the list loads, and stay that way if the request fails (`.catch(() => [])`), so someone could remove picks that still exist. Could we wait for a successful load, like `ProductConditionForm` does with `savedLoaded`?
> 4. This still says thirty-five condition types, and the list is missing Projects (after Products). Should be thirty-six now.

What changed: the body sets the weight once, so no comment repeats it; comments open differently (question, observation, plain correction); each keeps its trigger, visible effect and fix hint; hedge tails and caveat clauses are gone.

Other summary bodies that read as human:

> Looks good to me, just some nits.

> One real issue on the retry loop, the rest are small.

> Couple of questions before I approve.

## PR/MR description

Bad:

> ## Summary
> This PR introduces a comprehensive enhancement to our caching layer. It's not just a performance improvement, it's a fundamental shift in how we handle data.
> ## Changes
> - **Caching:** Added caching.
> - **Tests:** Added tests.
> ## Conclusion
> Overall, this change significantly improves performance and maintainability.

Good:

> Caches product prices for 5 minutes so the checkout page stops calling the pricing service on every render. p95 checkout load dropped from 1.8s to 0.6s on staging.
>
> Prices can now be up to 5 minutes stale. Promotions already publish 10 minutes ahead, so this does not affect them.
>
> Closes #412.

## Bug report

Bad:

> I've encountered an issue where the export functionality doesn't seem to be working as expected. It would be great if someone could take a look at this when they have a chance.

Good:

> CSV export returns an empty file for accounts with more than 10k orders.
>
> 1. Log in as an account with 10k+ orders (staging: `demo-large`).
> 2. Orders -> Export -> CSV.
>
> Expected: file with all orders. Actual: 0-byte file, and the API logs `timeout after 30000ms` for `/exports`. Started after the 3.4.0 deploy; smaller accounts are fine.

## Ticket with acceptance criteria

Good:

> Customers can't tell why a payment failed, so they contact support instead of retrying. Show the decline reason on the failed payment screen.
>
> Acceptance criteria:
> - Card declines show the reason the provider returns (insufficient funds, expired card, and so on).
> - Unknown reasons show "Your bank declined the payment" plus a retry button.
> - Raw provider error codes never reach the customer.

Bullets fit here: the criteria are parallel and each is tested separately.

## Status update

Bad:

> Hi team! Just wanted to give a quick update on where things stand. I've been working hard on the migration and have made significant progress. There are a few blockers I'm navigating, but overall things are moving forward nicely!

Good:

> Migration is 70% done (orders and invoices moved). Blocked on read access to the legacy payments DB; @dana, can you grant it? Without it, Friday slips to Tuesday.

## Chat message

Bad:

> Hey! Hope you're doing well. I was wondering if you might possibly have a moment at some point to take a look at my PR? No rush at all!

Good:

> Could you review #318 today? It's the fix for the double-charge bug, so I'd like it in before the 4pm deploy.

## Disagreeing in a thread

Bad:

> I completely understand your perspective and really appreciate the feedback! However, I respectfully believe that there might be some considerations that could potentially make the current approach preferable.

Good:

> I'd keep the retry here. The provider returns 503 for a few seconds during its deploys, and without the retry those orders fail outright. Happy to cap it at 3 attempts if the delay worries you.

## Unsure claim

Ask instead of asserting when you have not verified it.

> Does this run before the tenant scope is applied? If so, `Invoice.find(id)` could return another account's invoice.

## Secrets and customer data

Bad: pasting the full failing request, including the `Authorization` header and the customer's email.

Good:

> Requests with an expired token get 500 instead of 401:
>
> ```
> POST /api/orders  ->  500
> Authorization: Bearer [redacted]
> NoMethodError: undefined method `account' for nil
> ```

## Anti-pattern: shortened by dropping facts

Original note: CSV export fails with `timeout after 30000ms` for accounts over 10k orders since 3.4.0; small accounts work; repro account `demo-large`.

Bad (short but lossy):

> Export is broken, please fix.

Good: keep the error, the threshold, the version and the repro account. See "Bug report" above. Short means fewer words, not fewer facts.

## Anti-pattern: robot shorthand

Bad:

> Null deref L42. Session expired -> null. Fix: early return.

Good:

> This crashes when the session has expired: `fetchUser` returns `null` and line 42 reads `.id`. Could we return early?
