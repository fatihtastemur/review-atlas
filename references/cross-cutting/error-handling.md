# Error handling and reliability

Read this guide when changes alter failure behavior, retries, fallbacks, external
I/O, transactions, background work, or public error contracts.

## Preserve meaning across layers

Classify failures before handling them:

- invalid caller input;
- unauthenticated or unauthorized access;
- missing or conflicting state;
- transient dependency failure;
- permanent dependency rejection;
- programmer error or violated invariant;
- cancellation or deadline expiry.

Do not collapse these into an empty result or generic success. Translate errors at
boundaries where the consumer contract changes, preserve the original cause, and
avoid logging the same failure at every layer.

## Catching and recovery

- Catch only errors for which the current layer has a meaningful policy.
- A fallback must preserve security and correctness, not merely availability.
- Never turn corrupted, unauthorized, or ambiguous data into “not found.”
- Cleanup must run after partial initialization, early return, cancellation, and timeout.
- When cleanup fails, preserve both the primary failure and cleanup context where possible.
- Do not retry validation, authorization, deterministic business rejection, or malformed input.

## Retry review

Before accepting a retry, identify:

1. which failures are transient;
2. whether the operation is idempotent;
3. whether the previous attempt may have committed;
4. maximum attempts, delay, jitter, and total deadline;
5. load amplification and retry storms;
6. observability and terminal failure handling.

Retry the complete transaction or unit whose invariants must remain atomic. Retrying
only the final statement can preserve stale reads or duplicate earlier effects.

## Ambiguous outcomes

A timeout or broken connection after sending a request does not prove the server did
not commit it. State-changing operations should use idempotency keys, natural unique
constraints, operation records, or reconciliation when ambiguity matters.

## Public errors

- Keep machine-readable codes stable and human messages safe to change.
- Do not expose stack traces, SQL, internal paths, secrets, or personal data.
- Map cancellation and dependency timeout intentionally; they are not always server defects.
- Preserve correlation identifiers without trusting client-supplied values blindly.
- Document breaking changes to status codes, error types, and retryability.

## Background failures

- Fire-and-forget work needs an owner, durable delivery requirement, and terminal error path.
- Queue consumers need poison-message handling and bounded retries.
- Scheduled jobs must surface partial completion and safe restart behavior.
- Process-level handlers are a last-resort diagnostic boundary, not normal recovery.

## Review checklist

- [ ] Every catch block has a concrete recovery or translation policy.
- [ ] Causes, cancellation, and retryability remain distinguishable.
- [ ] Retries are bounded, jittered, and safe after ambiguous outcomes.
- [ ] Partial work and cleanup preserve invariants.
- [ ] Client errors are stable and do not leak internal data.
- [ ] Background failures are observable and recoverable.
