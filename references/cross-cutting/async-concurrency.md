# Async and concurrency review

Read this guide when changes create tasks, threads, goroutines, executors, channels,
queues, locks, parallel queries, background jobs, or shared mutable state.

## Establish the ownership model

For every concurrent activity, identify:

- who starts it;
- who can cancel it;
- who waits for completion;
- where errors are observed;
- which resources it owns;
- how shutdown terminates it;
- the maximum concurrency and queue size.

Missing ownership is a stronger finding than a stylistic preference for one primitive.

## Shared-state invariants

- Protect the complete invariant, not individual reads and writes.
- Check-then-act, read-modify-write, and lazy initialization require atomicity.
- Locks must use a consistent acquisition order and must not be held during slow external I/O.
- Thread-safe collections do not make compound workflows atomic.
- Immutable snapshots, message passing, or partitioned ownership may be simpler than shared locks.
- Verify memory visibility and safe publication under the language's memory model.

## Cancellation and deadlines

- Propagate cancellation through blocking work that can safely stop.
- Do not use an already-cancelled request token for mandatory rollback or cleanup.
- A timeout should bound the whole operation; stacked independent timeouts can exceed the user deadline.
- Cancellation after commit must not be reported as proof that no effect occurred.
- Ensure waiting producers and consumers wake during shutdown.

## Backpressure and resource limits

- Bound task creation, worker pools, queues, buffers, retries, and fan-out.
- Size concurrency against the scarcest downstream resource, not available CPU alone.
- Define overload behavior: reject, shed, queue, degrade, or block with a deadline.
- Avoid unbounded in-memory accumulation when a consumer slows or disappears.
- Rate limits should cover retries and distributed replicas, not only one process.

## Ordering and duplicate execution

- Do not assume completion order equals submission order.
- If ordering matters, state its key and scope explicitly.
- Queue redelivery and retries create at-least-once behavior unless proven otherwise.
- Idempotency storage must be atomic with the protected effect or support reconciliation.
- Exactly-once labels usually hide a narrower guarantee; inspect boundaries.

## Testing concurrent behavior

- Coordinate operations with barriers, latches, channels, or controlled fakes instead of sleeps.
- Force the race window and assert the protected invariant.
- Run race/thread sanitizers when supported.
- Verify cancellation, timeout, overload, shutdown, duplicate delivery, and error propagation.
- Keep test deadlines bounded so failures do not hang CI.

## Review checklist

- [ ] Every activity has ownership, termination, and error observation.
- [ ] Shared invariants are atomic under realistic interleavings.
- [ ] Cancellation and deadlines reach all blocking boundaries.
- [ ] Concurrency and buffering are bounded by downstream capacity.
- [ ] Ordering and duplicate-delivery assumptions are explicit.
- [ ] Tests deterministically exercise the race or lifecycle risk.
