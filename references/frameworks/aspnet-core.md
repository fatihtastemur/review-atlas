# ASP.NET Core review

Read this with the C# guide. Infer the target .NET and ASP.NET Core versions from
the project SDK and package references.

## Request pipeline and contracts

- Middleware order affects exception handling, forwarded headers, routing, CORS,
  authentication, authorization, rate limiting, and endpoint execution.
- Verify model binding and validation for body, route, query, form, and header inputs.
- Keep DTO validation distinct from domain invariants; do not bind persistence
  entities directly from untrusted requests.
- Review status codes, `ProblemDetails`, content types, route changes, and JSON
  options for compatibility.

## Authentication and authorization

- Require authorization on the endpoint or a secure fallback policy; do not rely
  only on UI visibility.
- Validate policy, role, claim, tenant, and resource ownership at the action being performed.
- Check scheme selection, token validation parameters, cookie security, antiforgery,
  CORS, forwarded-header trust, and open redirects.

## Dependency injection and lifetime

- Detect scoped services captured by singletons or used by background tasks after a request ends.
- Avoid building nested service providers during registration.
- Hosted services should create scopes deliberately, observe cancellation, report
  failures, and shut down within bounded time.

## EF Core and performance

- Keep `IQueryable` composition server-side until the intended materialization point.
- Review `Include` shape, projections, split queries, tracking, pagination, N+1 access,
  concurrency tokens, transactions, and cancellation.
- Do not return lazy or streaming results after the `DbContext` has been disposed.
- Ensure migrations are deployable with mixed application versions and realistic table size.

## Minimal APIs, MVC, and filters

- Confirm endpoint metadata contains the intended authorization, validation,
  content type, rate limit, antiforgery, and OpenAPI behavior.
- Endpoint filters, action filters, middleware, and exception handlers run at
  different layers; verify the chosen layer sees and handles the intended failures.
- Avoid accepting EF entities or broad command objects directly from requests.
- For streaming responses, confirm cancellation, disposal, partial-response errors,
  proxy buffering, and serialization lifetime.

## Authentication details

- Validate issuer, audience, signature algorithm, signing keys, expiry, clock skew,
  and scheme forwarding for bearer tokens.
- Cookie-based applications need secure cookie flags, antiforgery, session renewal,
  logout invalidation expectations, and shared Data Protection keys across replicas.
- Resource authorization must evaluate the loaded resource, not only a route role.
- Claims transformation and custom handlers must not perform unbounded or repeated I/O.

## Configuration and hosting

- Bind configuration to validated options and fail startup for required invalid values.
- Secrets should come from an approved provider and must not be copied into logs or client configuration.
- Respect reverse-proxy trust boundaries for forwarded headers, host filtering, HTTPS
  redirection, client IPs, and generated callback URLs.
- Health checks should distinguish liveness from dependency readiness and avoid leaking internals.
- Graceful shutdown must stop accepting work, drain owned queues, and respect host cancellation.

## EF Core review patterns

```csharp
// Risky: one query for orders and potentially one query per customer.
foreach (var order in await db.Orders.ToListAsync(cancellationToken))
{
    Console.WriteLine(order.Customer.Name);
}

// Prefer a bounded projection when only these fields are needed.
var summaries = await db.Orders
    .OrderBy(order => order.Id)
    .Select(order => new OrderSummary(order.Id, order.Customer.Name))
    .Take(limit)
    .ToListAsync(cancellationToken);
```

- Confirm whether lazy loading is enabled before claiming an N+1 query.
- `AsNoTracking` suits read-only work but not flows that expect automatic updates.
- Bulk update/delete operations bypass tracked entity callbacks and in-memory state.
- Retry execution strategies can replay a transaction; custom work must be idempotent.
- A `DbContext` is scoped and not thread-safe; do not share it across parallel tasks.
- Optimistic concurrency conflicts need a domain decision: reject, merge, or retry with fresh state.

## ASP.NET Core testing matrix

- Unit: domain policy and pure mapping.
- Integration: routing, middleware order, validation, filters, auth schemes, policies,
  serialization, options, and EF mappings.
- Database integration: provider-specific SQL, constraints, transactions, concurrency,
  migrations, and query count.
- Contract: externally consumed request/response and event schemas.
- Operational: startup failure, health checks, graceful shutdown, and configuration overrides.

## ASP.NET Core checklist

- [ ] Pipeline order and endpoint metadata enforce the intended policy.
- [ ] Resource authorization and tenant scoping cannot be bypassed.
- [ ] DI lifetimes and background services respect ownership.
- [ ] EF queries are bounded, server-evaluated, and transactionally correct.
- [ ] Proxy, cookie, token, CORS, and antiforgery configuration matches deployment.
- [ ] Public API and serialization changes remain compatible.
