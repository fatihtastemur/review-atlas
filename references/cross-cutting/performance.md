# Performance review

Report performance issues only when the changed code plausibly affects production
latency, throughput, memory, cost, or availability. State the workload that triggers
the problem.

## I/O and data access

- Detect N+1 queries or network calls inside loops and per-item lazy loading.
- Avoid selecting or deserializing unused large fields and unbounded result sets.
- Verify filters, joins, sort order, and pagination can use appropriate indexes.
- Prefer set-based work while preserving authorization and transaction semantics.
- Check timeout, cancellation, retry, backoff, and connection-pool behavior.

## CPU and memory

- Look for accidental quadratic behavior, repeated parsing, reflection, regex
  compilation, and serialization in hot paths.
- Avoid materializing multiple full copies of large sequences or payloads.
- Treat unbounded queues, caches, buffers, goroutines, tasks, and thread pools as
  availability risks.
- Verify streams and disposable resources are closed on success, failure, and cancellation.

## Concurrency and caching

- Parallelism must be bounded relative to the downstream resource.
- Shared mutable state needs a clear synchronization and ownership model.
- Cache keys must include tenant, authorization, locale, and other dimensions that
  change the result.
- Review invalidation, stampede behavior, stale data tolerance, and fallback when
  the cache is unavailable.

Ask for a benchmark only when the decision depends on measurements. Never present
an estimated speedup as observed evidence.

## Establish a performance case

A valid finding connects code to a realistic workload:

- request or job frequency;
- expected input and result cardinality;
- concurrency and downstream limits;
- algorithmic or I/O growth;
- allocation and retained-memory behavior;
- latency, throughput, cost, or availability impact.

Do not report a micro-optimization in cold code as a defect.

## Database and network cost

- Count round trips, not only loop iterations.
- Batch only to a bounded size supported by provider parameter and payload limits.
- Parallel calls can reduce latency while exhausting pools or triggering rate limits.
- Reuse clients and pools according to their lifecycle contract.
- Apply connect, request, read, transaction, and total deadlines coherently.
- Compression trades bandwidth for CPU and may amplify decompression attacks.
- Retries multiply traffic; include them in capacity calculations.

## Algorithm and allocation review

- Look for nested scans, repeated sorting, repeated parsing, and linear membership checks.
- Confirm big-O claims against actual collection types and expected sizes.
- Avoid converting streams to full in-memory collections without a bounded reason.
- Reused buffers and pools need clear ownership to prevent corruption or data disclosure.
- Large-object allocation, retained backing arrays, and caches can increase pause or memory pressure.
- Logging and telemetry in hot loops can dominate work and cost.

## Cache review

- Define the source of truth and tolerated staleness.
- Keys must include all result dimensions and use bounded cardinality.
- Set size, eviction, TTL, negative caching, and invalidation policy explicitly.
- Prevent stampedes with coalescing, jitter, or bounded refresh.
- A distributed cache adds network and serialization cost; measure the full path.
- Never let cache fallback weaken authorization or tenant isolation.

## Measurement quality

- Prefer production traces, query plans, profiles, and representative benchmarks.
- Warmup, JIT, caches, data distribution, concurrency, and environment affect results.
- Compare end-to-end behavior and resource use, not only an isolated operation.
- Record baseline, method, dataset, variance, and regression threshold.

## Performance checklist

- [ ] The affected path and triggering scale are identified.
- [ ] I/O count, query shape, result bounds, and pool limits are known.
- [ ] CPU complexity and allocation claims match actual data structures.
- [ ] Parallelism, queues, retries, and caches are bounded.
- [ ] Suggested improvements preserve correctness and security.
- [ ] Performance claims are measured or clearly labeled as hypotheses.
