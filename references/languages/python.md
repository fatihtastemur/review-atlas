# Python review

Infer the supported Python versions, type checker, formatter, framework, and
dependency manager from project configuration.

## Values and typing

- Avoid mutable default arguments and shared class-level mutable state.
- Check truthiness where empty, zero, false, and missing have different meanings.
- Type narrowing, `Optional`, protocols, and generics should match runtime behavior;
  casts must not hide reachable invalid values.
- Preserve iterator and generator semantics; avoid consuming them twice or returning
  a generator tied to a closed resource.

## Exceptions and resources

- Catch the narrowest useful exception and preserve causes with `raise ... from ...`.
- Do not suppress cancellation or convert programmer errors into normal absence.
- Use context managers for files, locks, transactions, temporary resources, and clients.
- Ensure cleanup works when iteration stops early or an async task is cancelled.

## Async and concurrency

- Do not call blocking I/O or CPU-heavy work directly on an event loop.
- Await created tasks or give background tasks explicit ownership and error reporting.
- Protect shared mutable state across threads, processes, tasks, and callbacks.
- Bound task creation, executors, queues, retries, and external concurrency.

## Security and data

- Avoid unsafe pickle or YAML loading, `eval`, shell interpolation, and untrusted template execution.
- Parameterize database operations and validate dynamic identifiers separately.
- Review timezone-aware datetimes, decimal precision, Unicode normalization, and serialization compatibility.
- Watch ORM N+1 access, implicit lazy loads, bulk-operation hook bypass, and transaction scope.

## Runtime and packaging discovery

Inspect `pyproject.toml`, lock files, supported Python versions, dependency groups,
type-checker strictness, formatter/linter settings, framework configuration, and
deployment model. Do not suggest syntax unavailable to the declared minimum version.

## High-signal bug patterns

### Shared mutable defaults

```python
# Risky: every call shares the same list.
def collect(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items

# Safer: allocate per call.
def collect(item: str, items: list[str] | None = None) -> list[str]:
    result = [] if items is None else items
    result.append(item)
    return result
```

Check dataclass and Pydantic field defaults, class attributes, caches, and test fixtures
for equivalent shared state.

### Blocking work runs on the event loop

```python
async def handler() -> bytes:
    return requests.get(upstream_url, timeout=5).content
```

Confirm the client is synchronous and the function runs on an event loop before
reporting. Prefer an async client or deliberate thread/process offload with cancellation.

## Data model and API contracts

- Dataclass equality, ordering, hashing, frozen behavior, slots, and default factories
  must match identity and mutation rules.
- Protocols and type hints do not validate runtime input unless a framework explicitly does so.
- Avoid broad `Any`, unchecked casts, and `# type: ignore` that hide reachable bad states.
- Iterators are one-shot; logging, validation, or length checks can consume them before use.
- Dictionary merge order, pattern matching, and enum serialization can become public contracts.
- Use timezone-aware datetimes and `Decimal` where domain precision requires them.

## Exceptions, cleanup, and concurrency

- `finally` returns can suppress exceptions; bare `except` can swallow cancellation and shutdown signals.
- Async generators and context managers require cleanup when consumers stop early.
- A created task must be awaited, retained, or owned by a supervised task group.
- Thread-safe does not imply process-safe or async-safe; identify the actual concurrency model.
- Multiprocessing requires serialization-safe state and guarded process entry points.
- Bound queues and worker creation; propagate backpressure instead of accumulating work indefinitely.

## Security review prompts

- Prefer safe YAML loaders and never unpickle untrusted data.
- Use subprocess argument lists without `shell=True` for untrusted values.
- Validate archive members and filesystem targets against traversal and symlink attacks.
- Parameterize SQL and review ORM raw-expression escape hatches.
- Treat template autoescape bypasses, redirects, host headers, URLs, and proxy headers as trust boundaries.
- Prevent secrets and personal data from entering tracebacks, structured logs, reprs, or debug pages.

## Testing expectations

- Use focused unit tests for pure functions and integration tests for framework,
  database, serialization, timezone, async, and authorization behavior.
- Assert exceptions and side effects rather than only status codes or mock calls.
- Async tests should expose leaked tasks and close clients, sessions, and event loops cleanly.
- Test cancellation, retries, duplicate delivery, transaction rollback, and mixed schema versions.

## Python review checklist

- [ ] Declared Python versions support syntax and dependencies.
- [ ] Defaults, class state, iterators, and closures do not leak mutable state.
- [ ] Async paths contain no accidental blocking work or orphaned tasks.
- [ ] Exceptions preserve causes and cleanup.
- [ ] Deserialization, commands, paths, templates, queries, and URLs are safe.
- [ ] ORM loading and result sizes are bounded and transactionally correct.
