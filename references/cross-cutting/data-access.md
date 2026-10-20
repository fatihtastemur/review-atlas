# Data access, transactions, and N+1 review

Read this guide when changes use an ORM, repository, query builder, transaction,
cache-backed read, batch job, or remote data service.

## Trace actual I/O

Do not infer database behavior only from object-oriented code. Determine:

- when a query is executed;
- how many times it executes;
- selected columns and expected rows;
- whether relationships load eagerly, lazily, or in batches;
- transaction, connection, and cursor lifetime;
- provider-specific SQL and parameter behavior.

## N+1 detection

An N+1 finding needs evidence of per-item I/O:

```text
load parents once
for each parent:
    load children separately
```

Confirm lazy loading, repository calls, serializers, template access, or nested
resolvers actually trigger I/O. Resolve with a projection, eager load, batch query,
DataLoader-style batching, or redesigned endpoint according to cardinality. A giant
join can be worse than bounded split queries, so include row multiplication and payload size.

## Query safety and bounds

- Parameterize values. Dynamic identifiers require strict allow-lists.
- Apply authorization and tenant filters before materialization.
- Bound list endpoints and batch operations; pagination needs stable unique ordering.
- Avoid selecting large unused fields or loading entire aggregates for a scalar check.
- Keep predicates compatible with column types, collations, and useful indexes.
- Treat suggested indexes as hypotheses until plans and data distribution support them.

## Transaction boundaries

- Group writes that must preserve one invariant and exclude unrelated slow work.
- Do not assume repository or save calls create the intended transaction.
- Handle rollback, commit failure, connection loss, deadlock, serialization failure,
  and optimistic concurrency according to the domain.
- External side effects cannot be atomically rolled back with an ordinary database transaction.
- Use outbox/inbox, idempotency, sagas, or reconciliation when cross-system consistency matters.

## Lost updates and duplicate writes

- Read-then-write without a version check can overwrite concurrent changes.
- Check constraints, conditional updates, row versions, and lock scope.
- Idempotency keys need request identity, result retention, conflict semantics, and expiry.
- Unique constraints are the final concurrent guard for uniqueness; pre-checks improve UX only.
- Retrying a transaction must not duplicate messages, emails, charges, or audit events.

## Cache interaction

- Cache keys must include every dimension that changes the result, especially tenant and authorization.
- Define invalidation and consistency tolerance before introducing caching.
- Prevent stampedes and unbounded key cardinality.
- Cache failure should not bypass security or return another principal's data.

## Review checklist

- [ ] Query count and execution points are understood.
- [ ] Results are authorized, tenant-scoped, bounded, and deterministically ordered.
- [ ] Transactions match business invariants and cross-system effects.
- [ ] Concurrency control prevents lost updates and duplicate operations.
- [ ] Index advice is supported by plans and representative data.
- [ ] Cache keys, invalidation, isolation, and fallback are safe.
