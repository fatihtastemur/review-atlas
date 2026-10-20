# Spring Boot review

Read this with the Java guide. Infer the Spring Boot major version because Jakarta
package names, defaults, security configuration, and supported Java versions differ.

## Web and validation

- Validate request bodies, path variables, query parameters, headers, and multipart limits.
- Keep transport DTOs separate from JPA entities to avoid over-posting and persistence leakage.
- Review status codes, exception handlers, content negotiation, serialization, and API compatibility.
- Treat proxy-related annotations such as `@Transactional`, `@Async`, and `@Cacheable`
  carefully: self-invocation and non-proxied instances bypass advice.

## Security

- Verify route matchers, method security, resource ownership, tenant scope, CSRF,
  CORS, session policy, password encoding, and token validation.
- Ensure actuator, management, documentation, and error endpoints do not expose
  sensitive information publicly.
- Do not trust client-provided IDs, roles, prices, or ownership fields.

## Transactions and persistence

- Make transaction boundaries explicit at the use-case layer; checked exceptions and
  caught exceptions can change rollback behavior.
- Review propagation, isolation, read-only assumptions, lazy access, N+1 queries,
  locking, pagination, cascades, orphan removal, and bulk-update persistence-context drift.
- Avoid remote calls inside long database transactions unless atomicity and timeout
  behavior are deliberately designed.

## Configuration and operations

- Prefer validated typed configuration; fail clearly on invalid production settings.
- Check bean ambiguity, conditional configuration, circular dependencies, and scope mismatches.
- Bound executor and connection pools and align timeouts across HTTP, database, queue,
  transaction, and load-balancer layers.

## MVC, WebFlux, and request handling

- Do not mix blocking database or HTTP clients into reactive event-loop paths.
- In MVC, async return types still need bounded executors, cancellation, and context propagation.
- Validate nested request objects and collection elements, not only the top-level DTO.
- Central exception handling must preserve status, stable error shape, traceability,
  and safe client messages without exposing internal exception data.
- Multipart, decompression, request size, and parsing limits should apply before expensive work.

## Spring Security details

- Matcher order and path semantics can leave endpoints unintentionally public.
- Method security should complement, not silently contradict, HTTP security.
- Verify resource ownership and tenant context inside the trusted service boundary.
- JWT validation needs signature, issuer, audience, expiry, algorithm, and key rotation.
- Cookie sessions require CSRF, fixation protection, secure cookie flags, and logout semantics.
- CORS is not an authorization mechanism; credentials and wildcard origins are a dangerous combination.

## Proxy and annotation traps

```java
@Service
class BillingService {
    public void bill(Order order) {
        chargeInTransaction(order); // Self-invocation can bypass transactional advice.
    }

    @Transactional
    void chargeInTransaction(Order order) {
        // ...
    }
}
```

Confirm proxy mode, method visibility, bean ownership, and call path. The same class
of issue affects async, caching, retry, and authorization annotations.

## JPA and Hibernate review patterns

- Fetch joins over multiple collections can multiply rows and distort pagination.
- `open-in-view` can hide persistence access in serialization and templates.
- Entity callbacks and cascades should not perform network I/O or create surprising writes.
- Bulk JPQL or native updates bypass the persistence context and can leave managed entities stale.
- `save` does not define the transaction boundary; review the surrounding service method.
- Pessimistic locks, optimistic versions, and unique constraints solve different races.
- Generated SQL, query count, and plans require representative integration tests.

## Messaging, scheduling, and retries

- Consumers must define acknowledgement timing, duplicate handling, ordering, poison
  message behavior, and dead-letter policy.
- Retryable methods must be idempotent or protected by a durable idempotency key.
- Scheduled jobs need single-run or partitioning semantics in multi-replica deployments.
- Preserve tracing and security context intentionally across async execution.

## Spring Boot testing matrix

- Unit: domain policy without a Spring context.
- Slice: controller, JSON, validation, repository mapping, or security configuration.
- Integration: transactions, real database behavior, complete filter chain, messaging,
  and configuration binding.
- Contract: request/response, events, configuration, and generated clients.
- Operational: startup, actuator exposure, graceful shutdown, and dependency failure.

## Spring Boot checklist

- [ ] Boot, Java, Jakarta, and dependency generations are compatible.
- [ ] Proxy-backed annotations execute on the real call path.
- [ ] Security matchers, method rules, ownership, and tenancy agree.
- [ ] Blocking work does not enter reactive or undersized executor paths.
- [ ] JPA loading, transaction, locking, and pagination behavior is intentional.
- [ ] Consumers, retries, and scheduled work are idempotent and observable.
