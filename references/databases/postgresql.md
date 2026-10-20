# PostgreSQL review

Infer the PostgreSQL version, extensions, migration tool, and connection-pooling mode
before applying version-specific behavior.

## Schema and types

- Prefer domain-appropriate types such as `timestamptz`, `numeric`, UUID, arrays, or
  JSONB deliberately; application parsing must preserve their semantics.
- Use constraints, partial uniqueness, exclusion constraints, and foreign keys to
  protect invariants that must survive concurrent writers.
- Review enum evolution, sequence ownership, identity behavior, generated columns,
  collation, and extension availability across environments.

## Queries and indexes

- Parameterize values; dynamic identifiers require strict allow-lists.
- Match B-tree column order and partial-index predicates to actual query conditions.
- Consider GIN, GiST, BRIN, expression, and covering indexes only for demonstrated query shapes.
- Check implicit casts, functions on indexed columns, JSONB operators, row estimates,
  deep offsets, N+1 calls, and missing deterministic ordering.

## Transactions and concurrency

- Understand MVCC snapshots, isolation level, write skew, row locking, deadlock retry,
  and the distinction between statement and transaction time.
- Avoid idle-in-transaction sessions and long transactions that delay vacuum.
- Use advisory locks only with a documented key space, ownership, timeout, and cleanup plan.

## Migrations and operations

- Large table rewrites, index builds, constraint validation, and lock acquisition can
  block production traffic; use online-safe sequences where supported.
- Review connection pool size, transaction pooling limitations, statement timeouts,
  search paths, row-level security, and replication behavior.
- Expand contracts before removing columns, values, or behavior used by older deployments.

## Query review method

1. Establish cardinality, frequency, row width, and required ordering.
2. Inspect current indexes, statistics quality, and a representative `EXPLAIN` plan.
3. Distinguish estimated plans from `EXPLAIN ANALYZE`, which executes the query.
4. Check row-estimate errors, loops, heap fetches, spills, parallelism, and lock impact.
5. Include index write cost, vacuum work, storage, and cache pressure in the decision.

## Common failure patterns

- `NOT IN` with a null can produce no matches; use semantics that handle null intentionally.
- `timestamp without time zone` does not retain an offset; define the application convention.
- `now()` is stable for the transaction, not a changing wall clock.
- Sequence increments are not rolled back and must not imply gapless business numbering.
- Case-insensitive search, locale, Unicode normalization, and collation can disagree across layers.
- JSONB containment and path queries need operator-compatible indexes and stable schemas.
- Offset pagination is unstable under concurrent changes and expensive at depth.
- Row-level security depends on role, policy, owner bypass, and session context configuration.

## MVCC and locking

- Read committed, repeatable read, and serializable prevent different anomalies.
- Serializable transactions must retry the whole unit after serialization failure.
- `SELECT ... FOR UPDATE SKIP LOCKED` is useful for queues but can starve rows without policy.
- Advisory locks are not row locks and require consistent acquisition and connection ownership.
- Long snapshots and idle transactions retain dead tuples and delay vacuum progress.
- DDL lock acquisition can block behind old transactions even when the operation is fast.

## Migration safety

- Use concurrent index operations where appropriate, while accounting for failure cleanup and limitations.
- Add constraints as not valid and validate separately when that reduces lock risk.
- Split schema changes, backfills, and enforcement into observable, restartable phases.
- Never assume a rollback can instantly restore data removed or transformed by a migration.
- Test extension, collation, role, ownership, and search-path requirements in clean environments.

## PostgreSQL checklist

- [ ] Types, precision, collation, time, and null semantics match the domain.
- [ ] Constraints and isolation protect concurrent invariants.
- [ ] Plans are evaluated with representative cardinality and existing indexes.
- [ ] Pooling mode, session state, prepared statements, and timeouts are compatible.
- [ ] Migrations minimize locks and support mixed versions.
- [ ] Vacuum, replication, and disk consequences are considered.
