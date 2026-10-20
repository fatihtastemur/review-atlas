# Review checklist

Use this after the evidence-driven review. A checked category means it was
considered where relevant; it does not require a comment.

## Correctness

- [ ] Changed behavior matches the apparent contract and all callers.
- [ ] Null, empty, boundary, overflow, partial-failure, and retry cases are safe.
- [ ] Errors are propagated, translated, logged, and retried intentionally.
- [ ] Async work, cancellation, timeouts, and resource lifetimes are correct.
- [ ] Tests exercise behavior rather than implementation details.

## Security and privacy

- [ ] Authentication and authorization are enforced at the trusted boundary.
- [ ] User-controlled data is validated and encoded for its destination.
- [ ] Queries, commands, paths, templates, and URLs resist injection.
- [ ] Secrets and sensitive data do not enter source, logs, errors, or telemetry.
- [ ] Multi-tenant data access remains scoped to the current tenant or principal.

## Data and compatibility

- [ ] Schema and API changes are backward-compatible or safely migrated.
- [ ] Transactions preserve invariants across all writes.
- [ ] Query shape, indexes, cardinality, and pagination are appropriate.
- [ ] Serialization, time zones, precision, collation, and identifier handling are explicit.

## Architecture and maintainability

- [ ] Dependency direction respects existing boundaries.
- [ ] Domain rules are not duplicated across controllers, handlers, or adapters.
- [ ] Abstractions have more than speculative value and preserve substitutability.
- [ ] Configuration and dependency injection fail clearly when invalid.

## Performance and operations

- [ ] Hot paths avoid N+1 I/O, unbounded work, and accidental materialization.
- [ ] Concurrency is bounded and shared state is synchronized correctly.
- [ ] Caches have safe keys, invalidation, isolation, and failure behavior.
- [ ] Logs, metrics, and traces support diagnosis without exposing sensitive data.
- [ ] Rollout, rollback, and mixed-version operation are safe where relevant.

## Language and framework

- [ ] Declared runtime and dependency versions support the changed APIs and syntax.
- [ ] Framework lifecycle, middleware/filter order, scopes, and proxy behavior are correct.
- [ ] Serialization, validation, error handling, and cancellation follow project contracts.
- [ ] Generated code, build tags, analyzers, and compiler settings were considered.

## Database

- [ ] Query count and materialization points are understood.
- [ ] Existing constraints and indexes were inspected before proposing new ones.
- [ ] Concurrent writes cannot violate uniqueness or overwrite newer state.
- [ ] Deadlock, serialization, ambiguous commit, and retry behavior are safe.
- [ ] Migrations are bounded, observable, reversible where possible, and rollout-compatible.
- [ ] Replication, sharding, read concern, or replica lag matches the consistency contract.

## API and distributed systems

- [ ] Old and new producers, consumers, schemas, and stored data can coexist.
- [ ] Events define duplicate, ordering, partitioning, replay, and poison-message behavior.
- [ ] Cross-system effects use idempotency, outbox/inbox, compensation, or reconciliation.
- [ ] Deadlines, retries, circuit behavior, and fallbacks do not amplify failure.

## Test quality

- [ ] A bug fix has a regression test that fails without the fix.
- [ ] Assertions prove behavior and important non-effects.
- [ ] Integration boundaries use real behavior where mocks are insufficient.
- [ ] Concurrency tests coordinate the race instead of relying on sleeps.
- [ ] Tests control time, randomness, locale, identifiers, and external dependencies.
- [ ] Existing tests were not weakened merely to accept changed behavior.

## Finding quality gate

Before reporting any finding, confirm:

- [ ] The changed code introduced or exposed the problem.
- [ ] A realistic triggering condition is described.
- [ ] User, system, security, or data impact is concrete.
- [ ] The referenced location is precise and actionable.
- [ ] Surrounding code, framework behavior, validation, tests, or constraints do not prevent it.
- [ ] Severity reflects both impact and likelihood.
- [ ] The finding is not a duplicate, formatter issue, or personal preference.
