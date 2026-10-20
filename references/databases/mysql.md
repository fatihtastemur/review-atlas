# MySQL review

Infer the MySQL or compatible-engine version, SQL mode, character set, collation,
storage engine, and migration tool before making version-specific claims.

## Schema and data integrity

- Choose integer signedness, string length, decimal precision, and temporal types
  from domain constraints rather than sample data.
- Keep application and database character sets and collations compatible; review
  case sensitivity and index-length consequences.
- Use foreign keys, unique constraints, and checks where they protect real invariants.
- Treat zero dates, implicit conversions, and permissive SQL modes as compatibility risks.

## Queries and indexes

- Parameterize values and allow-list identifiers used for sorting or dynamic table selection.
- Match composite index order to selective equality predicates, ranges, joins, and ordering.
- Watch functions or type coercion on indexed columns, leading-wildcard searches,
  unbounded scans, offset pagination at depth, and `SELECT *` on wide rows.
- Verify query plans with production-like cardinality before claiming an index solves a problem.

## Transactions and migrations

- Check isolation-level effects, gap locks, deadlocks, retry behavior, and consistent lock order.
- Keep transactions short and avoid network calls while locks are held.
- Review online DDL support, table rebuilds, backfill duration, replication lag, and rollback strategy.
- Use expand-and-contract migrations when old and new application versions coexist.

## Query review method

1. Identify expected cardinality, frequency, row width, and latency budget.
2. Inspect existing indexes and representative execution plans.
3. Verify predicate types and collations match indexed columns without coercion.
4. Check rows examined, temporary tables, filesort, join order, and selected columns.
5. Balance read benefit against write amplification, storage, and maintenance cost.

Do not declare an index missing from SQL text alone. Data distribution and the
existing index set determine whether it helps.

## Common failure patterns

- `utf8` may not represent the full Unicode range; check the actual character set.
- Comparing numeric columns with strings, or differently collated strings, can
  change results or index use.
- `NOT IN` behaves unexpectedly when the subquery can produce null.
- `REPLACE` is delete-plus-insert semantics, not a generic update.
- `INSERT ... ON DUPLICATE KEY UPDATE` may react to any matching unique key.
- Offset pagination becomes expensive and unstable at depth; keyset pagination
  needs a deterministic unique ordering.
- Reads from replicas can be stale after a write; request flows may require primary affinity.
- Auto-increment and generated keys do not by themselves prevent duplicate business operations.

## Locking and consistency

- Review the configured isolation level rather than assuming a default.
- Range predicates can acquire gap or next-key locks depending on isolation and indexes.
- Inconsistent row access order increases deadlock probability; retry the complete transaction.
- `SELECT ... FOR UPDATE` protects rows actually found, not arbitrary absent business keys.
- Unique constraints or explicit locking are required for concurrent uniqueness invariants.
- Keep external calls and user interaction outside transactions.

## Migration safety

- Adding a non-null column, changing type/collation, rebuilding an index, or rewriting
  a large table can block or saturate replicas depending on engine and version.
- Backfills should be resumable, bounded, observable, and separated from schema deployment.
- Introduce compatible readers before writers, then remove legacy fields in a later release.
- Validate replication format, lag, disk headroom, and rollback limitations.

## MySQL checklist

- [ ] Character set, collation, SQL mode, time zone, and engine are known.
- [ ] Constraints protect concurrent invariants.
- [ ] Queries are bounded and supported by measured plans.
- [ ] Transactions handle deadlocks, ambiguity, and idempotent retry.
- [ ] Migrations tolerate production table size and mixed application versions.
- [ ] Replica consistency matches the user-visible contract.
