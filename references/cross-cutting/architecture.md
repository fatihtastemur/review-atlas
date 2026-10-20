# Architecture review

Apply architecture guidance to changed boundaries and dependencies, not to
isolated naming or preferred folder layouts.

## Dependency direction

- Domain policy should not depend on HTTP, database, queue, or framework details.
- Application orchestration may depend on domain abstractions; adapters implement
  those abstractions at the edges.
- Flag a boundary violation only when it couples business behavior to volatile
  infrastructure, bypasses an invariant, or makes testing materially harder.

## SOLID checks

- **Single responsibility:** look for units changed for unrelated actors or reasons.
- **Open/closed:** prefer extension points only when variation is already real;
  reject speculative abstraction.
- **Liskov substitution:** implementations must preserve input, output, error,
  ordering, lifetime, and side-effect contracts.
- **Interface segregation:** consumers should not depend on operations they cannot
  use, but many tiny interfaces can also obscure a cohesive capability.
- **Dependency inversion:** policy should own abstractions at important boundaries;
  introducing an interface around every class is not a benefit by itself.

## Clean Architecture checks

- Controllers and handlers should translate transport concerns and delegate policy.
- Use cases should make transaction and authorization boundaries visible.
- Entities and value objects should protect invariants at construction and mutation.
- Persistence models must not silently define domain behavior or leak lazy loading.
- Cross-boundary models should be mapped deliberately when contracts differ.

## Change risks

Trace changes to public interfaces, events, DTOs, configuration keys, dependency
registrations, and database schemas through all producers and consumers. Consider
rolling deployments where old and new versions coexist.

## Cohesion and responsibility

Report mixed responsibilities when they create a demonstrated problem: unrelated
reasons to change, duplicated policy, unsafe transaction boundaries, hidden I/O,
or tests that must construct unrelated infrastructure. File or class size alone is
not evidence.

Prefer business capabilities over technical layers when that matches the repository,
but do not demand a structural rewrite for an isolated change. Locate invariants in
the narrowest shared boundary that every entry point must cross.

## Design-pattern review

Recommend a pattern only when it resolves an observed force:

- Strategy for genuinely interchangeable policies with growing conditionals.
- Factory when construction depends on validated variants or lifecycle ownership.
- Adapter when an external contract should not leak into application policy.
- Decorator for orthogonal behavior that must wrap several implementations consistently.
- State machine for explicit transitions that conditionals currently allow to drift.
- Outbox/inbox for reliable database-to-message coordination and duplicate delivery.

Name the current failure or maintenance risk, the simpler alternatives considered,
and the additional complexity. Do not treat repositories, mediators, factories, or
interfaces as automatic improvements.

## Boundary review questions

- Which layer owns validation, authorization, transactions, retries, and mapping?
- Can another entry point bypass the domain rule?
- Does an abstraction expose infrastructure-specific pagination, tracking, or exceptions?
- Are DTOs, entities, messages, and persistence models evolving on different schedules?
- Does dependency injection express required dependencies and valid lifetimes?
- Can the change be tested without reproducing framework internals?
- Is configuration validated before the first request or job uses it?

## Distributed architecture

- A network call is a partial-failure boundary, even inside one product.
- Define deadlines, retryability, idempotency, circuit behavior, and fallback semantics.
- Avoid synchronous call chains that multiply latency and availability dependencies.
- Events require schema evolution, ordering scope, duplicate handling, and replay safety.
- Eventual consistency needs an explicit user experience and reconciliation path.
- Service boundaries should follow independent ownership and change, not fashion.

## Architecture checklist

- [ ] Dependency direction keeps business policy independent from volatile adapters.
- [ ] Invariants are enforced at every relevant entry point.
- [ ] Abstractions correspond to real variation or a valuable boundary.
- [ ] Transactions and distributed effects have explicit ownership.
- [ ] Public and persistence contracts can evolve safely.
- [ ] The design remains observable, testable, and operable during failure.
