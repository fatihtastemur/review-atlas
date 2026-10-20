# Java review

Infer the Java version, build tool, compiler flags, framework, and nullness tooling
before relying on modern APIs or language features.

## Correctness and contracts

- Keep `equals` and `hashCode` consistent and stable for collection keys and ORM entities.
- Treat `compareTo` consistency, integer overflow, signed values, and narrowing conversions explicitly.
- Avoid returning mutable internal collections or using mutable objects as map keys.
- Use `Optional` for deliberate absence at API boundaries, not as a substitute for
  validation or as a mutable field container.

## Exceptions and resources

- Preserve causes when translating exceptions; do not catch broad exceptions and continue.
- Use try-with-resources for closeable resources, including exceptional paths.
- Keep checked-versus-runtime exception decisions consistent with existing contracts.
- Ensure interrupts are restored or propagated rather than swallowed.

## Concurrency

- Shared state requires safe publication and a clear thread-safety contract.
- `volatile` provides visibility but does not make compound operations atomic.
- Bound executors and queues; verify shutdown, rejection, timeout, and cancellation behavior.
- For virtual threads, still bound scarce downstream resources and avoid pinning operations.

## Streams and persistence

- Check stream reuse, side effects, ordering, parallel-stream safety, and accidental quadratic collectors.
- For JPA/Hibernate, review lazy access outside sessions, N+1 queries, cascade/orphan
  behavior, transaction demarcation, locking, pagination with fetch joins, and entity identity.

## Version and build discovery

Inspect the Maven or Gradle toolchain, release/source/target settings, dependency
management, annotation processors, module descriptors, static analysis, and test
platform. Distinguish legacy Java and Spring generations from modern code; package
names, language features, virtual threads, and framework defaults are not interchangeable.

## High-signal bug patterns

### Mutable identity breaks hash collections

```java
// Risky when id is assigned after the entity enters a HashSet.
@Override
public int hashCode() {
    return Objects.hash(id);
}
```

Trace when identifiers are assigned and whether equality crosses persistence
sessions. Do not prescribe one universal entity equality strategy.

### Transactions are bypassed or unintentionally committed

- Calls within the same instance may bypass proxy advice.
- A caught exception can allow a transaction to commit partial state.
- Rollback defaults can differ for checked and unchecked exceptions.
- Lazy reads after the transaction may fail or trigger hidden I/O.
- Remote calls inside transactions extend lock time and create ambiguous outcomes.

### Parallelism exceeds downstream capacity

```java
// Risky for an unbounded input when each task consumes a database connection.
orders.parallelStream().forEach(this::persist);
```

Check executor ownership, queue bounds, rejection behavior, interrupt handling,
context propagation, and shutdown. Virtual threads reduce thread cost, not database,
socket, memory, or rate-limit constraints.

## Language and API contracts

- Records are shallowly immutable; contained collections may still mutate.
- Sealed hierarchies and exhaustive switches must handle evolution across modules.
- `BigDecimal.equals` includes scale while `compareTo` does not; choose semantics deliberately.
- Avoid platform-default charset, locale, and time zone in persisted or signed data.
- `CompletableFuture` stages may run on an unintended executor and lose request context.
- Stream pipelines should not mutate shared state or rely on unspecified encounter order.
- Reflection, serialization, and native-image configuration need integration coverage.

## Security review prompts

- Check deserialization types, expression languages, template engines, XML parser
  features, archive extraction, redirects, URL fetches, file paths, and process execution.
- Parameterize JPQL, native SQL, and Criteria values; allow-list dynamic identifiers.
- Verify resource-level authorization and tenant filters are applied consistently,
  including repository methods, batch jobs, and message consumers.
- Review logging of tokens, headers, entity snapshots, personal data, and exception details.

## Testing expectations

- Prefer unit tests for pure policy and integration tests for transactions, mappings,
  validation, serialization, security chains, and database-specific behavior.
- Concurrency tests should coordinate threads with latches or barriers instead of sleeps.
- Verify rollback, duplicate delivery, retry, timeout, interrupt, and optimistic-lock conflicts.
- Test API consumers against old and new payloads when contracts evolve.

## Java review checklist

- [ ] Declared Java and framework versions support the implementation.
- [ ] Equality, hashing, comparison, precision, and time semantics are stable.
- [ ] Exceptions and interrupts retain their meaning.
- [ ] Executors, futures, streams, and resources have bounded ownership.
- [ ] Transactions and JPA loading occur within intentional boundaries.
- [ ] Serialization, authorization, and public contracts remain compatible.
