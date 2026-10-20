# Go review

Infer the Go version from `go.mod` and respect repository conventions enforced by
`go vet`, static analysis, and linters.

## Errors and APIs

- Check every meaningful error and preserve identity with `%w` when callers use `errors.Is` or `errors.As`.
- Add context without duplicating logs at every layer; log once where ownership is clear.
- Keep zero values useful where practical and document ownership of slices, maps, channels, and buffers.
- Avoid typed-nil values stored in interfaces and unintended pointer-to-loop-variable behavior.

## Context and concurrency

- Accept `context.Context` as the first parameter and propagate it to blocking I/O.
- Never store request contexts in long-lived structs.
- Every goroutine needs an owner, termination condition, and observable error path.
- Close channels from the sending side that owns them; avoid sends after close and blocked sends on abandoned consumers.
- Protect maps and shared state, including error and shutdown paths; run the race detector when warranted.

## Resources and performance

- Close response bodies, rows, files, and tickers; check deferred cleanup inside long loops.
- Bound worker pools, retries, request bodies, and collection growth.
- Beware subslices retaining large backing arrays and data races from reused buffers.
- In database code, check `rows.Err`, scan errors, transaction rollback, placeholder syntax, and context cancellation.

## Module and toolchain discovery

Inspect `go.mod`, `go.work`, build tags, generated files, cgo use, linter settings,
and supported platforms. Account for the declared Go version when reviewing loop
variables, standard-library APIs, generics, and module behavior.

## High-signal bug patterns

### Goroutine leak after a consumer exits

```go
// Risky: the sender blocks forever if the caller returns after the first result.
results := make(chan Result)
go func() {
    for _, item := range items {
        results <- process(item)
    }
}()
```

Look for cancellation-aware sends, bounded buffering, channel closure ownership,
and a wait path for every launched goroutine.

### Defer retains resources inside a long loop

```go
for _, name := range names {
    file, err := os.Open(name)
    if err != nil { return err }
    defer file.Close() // Runs only when the surrounding function returns.
}
```

Use a per-iteration helper when resources must be released promptly. Also check
HTTP response bodies and database rows for the same lifetime error.

## Error and interface contracts

- Do not compare wrapped errors with `==` when identity is part of the contract.
- Avoid logging and returning the same error at every layer; preserve useful context once.
- Named return values and deferred mutation can obscure the final result.
- An interface containing a typed nil is non-nil; examine constructors and mocks.
- Keep interfaces consumer-owned and minimal, but do not fragment cohesive behavior.
- Copy slices or maps when the caller must not observe later mutation.

## Concurrency and memory model

- A map is not safe for concurrent read/write without synchronization.
- Check whether a mutex protects the complete invariant rather than individual fields.
- Never copy a used mutex, wait group, once value, or atomic wrapper.
- Ensure timers and tickers are stopped when no longer needed.
- Cancellation must reach blocking channel operations, HTTP calls, database calls,
  and worker loops.
- Check closure capture and pointer aliasing against the declared Go version.

## HTTP, JSON, and security

- Bound request bodies before decoding and reject unexpected trailing JSON when contracts require it.
- Distinguish omitted, null, zero, and empty values in patch/update APIs.
- Configure HTTP client and server timeouts; the default client can wait indefinitely.
- Validate redirects, proxy headers, file paths, archive entries, and server-side URLs.
- Use `exec.Command` argument separation; never construct a shell command from input.
- Review `html/template` versus `text/template` and any deliberate unescaped HTML.

## Testing expectations

- Run table-driven tests for boundaries and error contracts.
- Use `go test -race` for changed concurrent code when the environment permits.
- Test cancellation and goroutine termination with bounded deadlines, not arbitrary sleeps.
- Use integration tests for SQL placeholder behavior, transaction semantics, HTTP
  middleware, and serialization contracts.

## Go review checklist

- [ ] Every goroutine, channel, timer, body, row set, and file has an owner.
- [ ] Errors retain identity and actionable context.
- [ ] Context reaches every blocking operation without being stored long term.
- [ ] Shared state follows the Go memory model.
- [ ] Inputs, collections, queues, retries, and concurrency are bounded.
- [ ] JSON, time, and zero-value semantics match the public contract.
