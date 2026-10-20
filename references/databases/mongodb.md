# MongoDB review

Infer the MongoDB server, driver, deployment topology, read/write concerns, and
schema-validation policy before evaluating behavior.

## Document design and integrity

- Embed data read and updated together; reference data with independent lifecycle
  or unbounded growth.
- Keep documents below size limits and prevent arrays or histories from growing without bounds.
- Validate required fields and types at trusted boundaries; account for older document versions.
- Use unique indexes or atomic conditional updates for invariants that concurrent writers must preserve.

## Queries and indexes

- Treat user-controlled query operators, field names, regexes, JavaScript, and pipeline
  stages as injection surfaces.
- Match compound index order to equality, sort, and range usage. Review multikey,
  partial, sparse, TTL, text, wildcard, and collation behavior explicitly.
- Avoid unanchored or catastrophic regular expressions, unbounded skips, full document
  fetches, and aggregation stages that exceed memory or spill unexpectedly.
- Ensure pagination has stable ordering and a deterministic tie-breaker.

## Atomicity and consistency

- Single-document writes are atomic; multi-document workflows need explicit handling
  for partial failure, retries, compensation, or transactions.
- Make updates idempotent when drivers retry writes. Check optimistic concurrency filters.
- Choose read preference, read concern, write concern, and causal consistency according
  to the business guarantee rather than latency alone.

## Operations and migrations

- Review shard keys for cardinality, distribution, monotonic growth, targeted queries,
  and tenant hot spots.
- Deploy schema changes with mixed document and application versions in mind.
- Background backfills need checkpoints, bounded batches, observability, and safe restart behavior.

## Query review method

1. Establish document count, field cardinality, selectivity, array growth, and working set.
2. Inspect current indexes and representative `explain` output.
3. Compare keys examined, documents examined, returned rows, sort, and fetch behavior.
4. Check whether collation, partial filters, sparse fields, or multikey expansion change applicability.
5. Include index storage, write amplification, memory, and shard routing costs.

## Common failure patterns

- Accepting arbitrary JSON filters can expose operators such as `$where`, `$regex`,
  or comparison operators and bypass intended equality checks.
- A unique index treats missing and null values according to its exact sparse or
  partial configuration; verify the real invariant.
- Positional array updates can affect a different element than intended when filters are incomplete.
- Replacing a document can silently remove fields written by newer application versions.
- Large `skip` values still scan past earlier results; range pagination needs stable sort keys.
- Natural order is not a public ordering contract.
- Unbounded arrays eventually create oversized documents and expensive rewrites.
- TTL deletion is asynchronous and must not be the only correctness or authorization control.

## Concurrency and transactions

- Use conditional updates with the previous version or state to prevent lost updates.
- Upserts need a unique index when duplicate creation must be impossible under races.
- Multi-document transactions cost more and do not replace good document boundaries.
- Retryable writes and transaction retries can re-enter application callbacks; keep
  external side effects outside or make them idempotent.
- Read preference and concerns determine whether a user can observe stale or rolled-back data.

## Sharding and migrations

- Queries missing the shard key may scatter to all shards.
- Monotonic or low-cardinality keys can create hot chunks and uneven load.
- Changing a shard key or correcting poor distribution is an operational project,
  not an ordinary schema edit.
- Readers should tolerate old and new document shapes during phased migrations.
- Backfills need deterministic selection, checkpoints, rate limits, retries, and validation counts.

## MongoDB checklist

- [ ] Document boundaries match atomicity and growth requirements.
- [ ] Query construction cannot accept unintended operators or fields.
- [ ] Indexes match filters, sort, collation, arrays, and shard routing.
- [ ] Concurrent updates protect versions and uniqueness.
- [ ] Read/write concern and retry semantics match business guarantees.
- [ ] Schema evolution and backfills tolerate mixed document versions.
