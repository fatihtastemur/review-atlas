# Common bug checklist

Use these patterns as investigation prompts, not automatic findings.

## Values and boundaries

- Off-by-one ranges, empty collections, negative values, overflow, truncation, and
  precision loss.
- Null or missing values treated differently across serialization, validation, and storage.
- Mutable default values or shared object instances leaking state between requests.
- Equality or hashing inconsistent with identity and mutation rules.

## Time and ordering

- Local time mixed with UTC, ambiguous daylight-saving transitions, and loss of offsets.
- Non-deterministic iteration order used for signatures, pagination, or user-visible results.
- Timestamp precision differences causing missed or duplicated incremental records.

## Failure and retry

- Exceptions swallowed, converted to success, or logged without changing control flow.
- Retries duplicating writes, extending transactions, or multiplying downstream load.
- Cleanup skipped on early return, cancellation, timeout, or partial initialization.
- Fallbacks masking corrupted or unauthorized data as missing data.

## Concurrency

- Check-then-act races, lost updates, stale reads, unsafe publication, and lock inversion.
- Background work outliving request-scoped dependencies.
- Loop variables or mutable references captured by asynchronous callbacks.

## Contracts

- New enum values, fields, or error variants breaking exhaustive consumers.
- Changed defaults or validation rules rejecting previously valid persisted data.
- Deletions leaving active call sites, configuration, migrations, or deployment references.
- Producer and consumer changes requiring an unsafe atomic deployment.

## Collections and pagination

- Modifying a collection while iterating or relying on unstable iteration order.
- Returning internal mutable collections that callers can change.
- Pagination without a unique stable order, causing duplicates or omissions.
- Offset and limit values that are negative, overflow, or permit unbounded reads.
- Deduplication that keeps an unintended item or loses meaningful ordering.

## Identity and authorization

- Comparing display names, emails, or mutable attributes as stable identifiers.
- Checking a role without checking ownership, tenant, scope, or resource state.
- Loading a resource by caller-provided tenant ID before verifying the authenticated tenant.
- Caching authorized data without principal or tenant dimensions in the key.
- Background jobs running without the authorization context assumed by request code.

## Data integrity

- Pre-checking uniqueness without a database constraint under concurrent writes.
- Read-modify-write updates without a version check or lock.
- Publishing an event before the transaction commits or losing it after commit.
- Retrying a charge, email, message, or insert without idempotency.
- Bulk operations bypassing validation, hooks, auditing, or optimistic concurrency.
- Partial batch success reported as complete success.

## Serialization and compatibility

- Unknown enum values crashing consumers or silently mapping to a privileged default.
- Missing and null fields treated as the same when patch semantics distinguish them.
- Numeric precision lost through floating-point or generic JSON types.
- Time offsets discarded or naive values interpreted in the server's local zone.
- Strict consumers rejecting newly added fields.
- Renamed fields breaking stored data, queued messages, signatures, or generated clients.

## Security-sensitive utilities

- Path validation performed before URL decoding or normalization.
- Redirect allow-lists based on substring matching.
- Regular expressions with attacker-controlled patterns or catastrophic backtracking.
- Random identifiers generated with predictable randomness.
- Secret comparisons using ordinary equality in sensitive flows.
- Logs containing headers, tokens, raw payloads, query text with values, or personal data.

## Operational bugs

- Readiness reports success before migrations, configuration, or critical dependencies are usable.
- Liveness depends on an external service and causes restart storms.
- Configuration defaults silently enable debug or insecure behavior in production.
- Graceful shutdown abandons queues, tasks, transactions, or in-flight requests.
- Metrics use unbounded labels such as user ID, URL, exception message, or request body.
- Clock skew and mixed timeout layers produce negative or unexpectedly long deadlines.

## Checklist discipline

For each pattern, locate an actual path from input and state to failure. Confirm the
framework, runtime, constraints, and surrounding code do not already prevent it.
Report one root cause rather than a separate finding for every manifestation.
