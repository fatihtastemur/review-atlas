# API and compatibility review

Read this guide when changes affect HTTP APIs, RPC, events, schemas, configuration,
public libraries, database contracts, or serialized state.

## Inventory consumers

Identify every producer and consumer, including older deployed versions, mobile
clients, third parties, jobs, replayed messages, stored documents, generated SDKs,
dashboards, and infrastructure configuration. Compatibility is defined by those
consumers, not only by whether current code compiles.

## Common breaking changes

- removing or renaming fields, endpoints, enum values, events, or configuration keys;
- making optional data required or narrowing accepted formats;
- changing null, empty, default, precision, time, ordering, or pagination semantics;
- changing status codes, error codes, retryability, or idempotency behavior;
- changing authentication schemes, scopes, ownership, or tenant interpretation;
- reusing a field with a different meaning;
- changing event partition keys or ordering guarantees;
- modifying library exceptions, side effects, threading, or resource ownership.

Adding a field can also break strict deserializers, exhaustive matches, signatures,
hashes, or clients that proxy schemas without preserving unknown data.

## Safe evolution patterns

- Add tolerant readers before new writers.
- Preserve old fields while introducing new representations.
- Dual-read or dual-write only with a reconciliation and removal plan.
- Version at a meaningful compatibility boundary, not for every implementation change.
- Use feature negotiation when clients upgrade independently.
- Deprecate with telemetry and an explicit removal criterion.
- Keep events immutable; publish a new type or version for incompatible semantics.

## Rolling deployment review

Test all relevant combinations:

- old application with old schema;
- new application with compatible old schema during rollout;
- old and new applications against the expanded schema;
- rollback after new data has been written;
- delayed or replayed old messages consumed by new code;
- new messages reaching old consumers.

## Contract verification

- Use schema or consumer-driven contract tests for externally owned contracts.
- Test unknown fields and enum values where forward compatibility is required.
- Preserve golden payloads only when they assert stable semantics, not incidental formatting.
- Validate generated clients and documentation from the same authoritative schema.
- Record intentional breaks and the migration path explicitly.

## Review checklist

- [ ] Producers, consumers, stored data, and deployment overlap are identified.
- [ ] Defaults, errors, ordering, time, precision, and null semantics remain compatible.
- [ ] Readers and writers are deployed in a safe sequence.
- [ ] Rollback remains possible after new data is produced.
- [ ] Contract tests cover old/new combinations and unknown values.
- [ ] Intentional breaks have versioning, migration, and communication plans.
