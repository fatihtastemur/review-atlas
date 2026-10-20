# C# and .NET review

Infer the target framework, language version, nullable context, analyzers, and SDK
from project files before applying version-specific guidance.

## Correctness and API design

- Respect nullable reference annotations across public boundaries; do not suppress
  warnings that represent reachable nulls.
- Check value equality for records, entities, structs, and dictionary keys.
- Ensure pattern matches and enum switches handle unknown or future values safely.
- Avoid exposing mutable collections or returning deferred queries beyond their
  valid data-context lifetime.

## Async and resources

- Prefer async all the way for I/O. Flag sync-over-async (`.Result`, `.Wait()`) when
  it can block or deadlock.
- Propagate `CancellationToken` through meaningful asynchronous operations.
- Await tasks whose failures matter; make intentional fire-and-forget work owned,
  observable, and independent of request-scoped services.
- Dispose `IDisposable` and `IAsyncDisposable` resources on every path. Do not
  dispose dependencies owned by the container.

## Collections, LINQ, and concurrency

- Watch repeated enumeration, client-side evaluation, hidden database calls, and
  `ToList` before filtering or pagination.
- Verify concurrent access to ordinary collections and mutable singleton state.
- Bound `Task.WhenAll` fan-out when each item consumes network, database, or CPU resources.

## Serialization and persistence

- Review JSON naming, required members, polymorphism, enum encoding, and backward compatibility.
- For EF Core, check tracking mode, query shape, N+1 access, concurrency tokens,
  transaction boundaries, and migrations that match model changes.
- Entity equality and hashing must remain stable while tracked and across generated IDs.

## Version and project discovery

Inspect `global.json`, `TargetFramework`, `LangVersion`, nullable settings,
implicit usings, package references, analyzers, trimming/AOT settings, and test
projects. Do not recommend an API or syntax that the declared toolchain cannot
compile. Treat warnings-as-errors and repository analyzers as part of the contract.

## High-signal bug patterns

### Deferred execution escapes its owner

```csharp
// Risky: enumeration happens after the DbContext may have been disposed.
public IEnumerable<Order> GetOpenOrders() =>
    db.Orders.Where(order => order.Status == OrderStatus.Open);

// Safer: execute within the owned lifetime and return a stable result.
public Task<List<OrderDto>> GetOpenOrdersAsync(CancellationToken cancellationToken) =>
    db.Orders
        .Where(order => order.Status == OrderStatus.Open)
        .Select(order => new OrderDto(order.Id, order.Total))
        .ToListAsync(cancellationToken);
```

Confirm the actual lifetime before reporting this pattern; returning `IQueryable`
inside a controlled repository abstraction may be intentional.

### Fire-and-forget uses request-scoped state

```csharp
// Risky: the request may finish before this task uses the scoped service.
_ = Task.Run(() => emailSender.SendAsync(message));
```

Look for disposed services, lost exceptions, missing cancellation semantics, and
process shutdown loss. Prefer an owned background queue or durable message when
delivery matters.

### Cancellation changes correctness

- Do not pass a cancelled request token to mandatory cleanup or compensation.
- Do pass cancellation through read-only or safely abortable I/O.
- Distinguish timeout from caller cancellation in logs and API responses.
- Verify cancellation after a committed write does not incorrectly report that
  the operation did not happen.

## API and type-system checks

- Public nullable annotations are compatibility metadata; changing `T` to `T?`
  or the reverse affects callers even when runtime signatures are identical.
- Required members, `init`, records, primary constructors, and collection
  expressions need toolchain-compatible behavior and serialization tests.
- Avoid `async void` except event handlers. Review event unsubscription and
  weak-reference requirements for long-lived publishers.
- Ensure `record` value equality is appropriate for entities with database identity.
- `DateTime.Kind`, `DateTimeOffset`, decimal scale, culture-sensitive parsing,
  and case comparison must match external and persistence contracts.
- Span-like values, pooled buffers, and ref structs must not outlive their backing storage.

## LINQ and performance traps

- Multiple terminal operations can execute the same database or expensive query repeatedly.
- `Any()` communicates existence; `Count() > 0` may force unnecessary counting.
- `Contains` over an unbounded in-memory collection can create oversized SQL or
  parameter-limit failures when translated by an ORM.
- `AsEnumerable()` switches remaining operators to client-side execution.
- Ordering must be deterministic before `Skip`/`Take`; include a stable tie-breaker.
- Avoid capturing mutable variables in parallel or deferred pipelines.

## Security review prompts

- Verify ASP.NET authorization at endpoints and at resource ownership boundaries.
- Treat `FromSqlRaw`, interpolated SQL, reflection, type loading, file paths,
  process invocation, regexes, XML parsers, and deserialization settings as sinks.
- Check mass assignment when request DTOs map broadly onto entities.
- Review Data Protection key persistence and sharing across replicas when cookies
  or protected payloads must survive restarts.
- Ensure logs do not serialize entire request, claims, tokens, connection strings,
  payment data, or personal records.

## Testing expectations

- Use unit tests for pure domain rules and integration tests for middleware order,
  model binding, authorization, serialization, EF mappings, and database behavior.
- A concurrency fix should include a test that coordinates the competing operations,
  not a timing-only sleep.
- Async tests must await the operation and assert the actual failure or result.
- Test cancellation, duplicate requests, optimistic concurrency conflicts, and
  mixed-version payloads when the change touches those contracts.

## C# review checklist

- [ ] Nullable annotations match reachable runtime values.
- [ ] Tasks, cancellation, and disposables have explicit ownership.
- [ ] DI lifetimes do not capture shorter-lived services.
- [ ] LINQ executes once, in the intended location, with bounded results.
- [ ] Serialization and public API changes remain compatible.
- [ ] EF Core queries, transactions, and concurrency behavior are verified.
- [ ] Culture, time, equality, and numeric semantics are explicit.
