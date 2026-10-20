# Test review

Read this guide when behavior changes, a bug is fixed, risk crosses an integration
boundary, or existing tests are modified.

## Match the test to the risk

- Unit tests: pure rules, branching, transformations, and invariant enforcement.
- Component tests: one service or module with controlled infrastructure boundaries.
- Integration tests: framework pipelines, databases, queues, files, serialization,
  transactions, migrations, and security configuration.
- Contract tests: independently deployed producers and consumers.
- End-to-end tests: a small number of critical user journeys and deployment wiring.

Do not replace a necessary integration test with mocks that reproduce the same
assumption as the implementation.

## Regression quality

A bug fix should include a test that fails for the original defect and passes for
the corrected behavior. The test should drive the public or meaningful boundary,
reproduce the triggering condition, and assert user-visible state or durable effects.

## Assertions and observability

- Assert outcomes, state transitions, emitted messages, persisted data, and errors.
- A test that only verifies a mock call may miss wrong arguments, transaction behavior,
  serialization, or downstream compatibility.
- Avoid assertions so broad that an error page, empty result, or fallback also passes.
- Verify negative effects when important: no unauthorized record, no duplicate message,
  no partial write, no secret in output.

## Determinism and isolation

- Control clocks, randomness, identifiers, locale, time zone, and external services.
- Do not use arbitrary sleeps for async behavior; synchronize on observable events.
- Isolate database state and avoid order-dependent shared fixtures.
- Keep retries and eventual-consistency waits bounded with useful failure diagnostics.
- Parallel test execution must not share ports, files, global configuration, or tenants unsafely.

## Boundary cases

Choose cases from the contract, not a ritual list:

- minimum, maximum, empty, null, missing, duplicate, and malformed values;
- time zones, DST transitions, precision, Unicode, locale, and case folding;
- cancellation, timeout, partial failure, retry, and ambiguous commit;
- concurrent update, duplicate delivery, stale version, and permission changes;
- old/new schemas, messages, configurations, and deployed versions.

## Review anti-patterns

- weakening or deleting an assertion only to accept changed behavior;
- snapshots that hide meaningful semantic regressions in large diffs;
- testing private methods instead of observable contracts;
- over-mocking the unit until no production wiring remains;
- tests that pass without awaiting asynchronous work;
- relying on the developer machine's database, clock, locale, or network.

## Review checklist

- [ ] Changed behavior and realistic failure paths are covered.
- [ ] The original bug would fail a regression test.
- [ ] Integration boundaries use real behavior where mocks are insufficient.
- [ ] Assertions prove outcomes and important non-effects.
- [ ] Tests are deterministic, isolated, bounded, and parallel-safe.
- [ ] Compatibility and concurrency risks have targeted coverage.
