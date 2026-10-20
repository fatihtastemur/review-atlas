---
name: review-atlas
description: Review Git diffs, branches, commits, pull requests, or selected code for concrete correctness, security, performance, architecture, and maintainability issues. Use for evidence-driven code review across C#/.NET, Java/Spring Boot, Go, PHP, Python, MySQL, PostgreSQL, and MongoDB. Do not use when the user only wants implementation or automatic fixes without a review.
license: MIT
metadata:
  short-description: Evidence-driven polyglot code review
---

# ReviewAtlas

Perform a findings-first code review. Review only; do not edit code, create
commits, or publish comments unless the user explicitly requests that separate
action.

Write all user-facing text in the user's preferred language, including scope
messages, helper options, findings, headings, questions, and the verdict. Resolve
the language from an explicit request, the conversation language, or
`git config --get review-atlas.language`, in that order. If none provides a
language, use the user's system locale when available, then fall back to English.
Keep code identifiers, file paths, commands, and quoted diagnostics unchanged.

## Workflow

1. Read [references/review-process.md](references/review-process.md).
2. Determine the requested review target. Prefer an explicit PR, commit range,
   branch, staged diff, or path. With no target, inspect the current branch:
   - On `main`, `master`, `test`, `stage`, `dev`, or `develop`, do not begin a
     review. Show the target helper from the review-process reference and ask
     which branch or target to review.
   - On any other named branch, treat `current` as selected. Detect its likely
     base and review only changes introduced by the current branch, plus its
     staged, unstaged, and untracked changes.
   State the resolved scope before reviewing. Ask for a base only when repository
   evidence remains genuinely ambiguous.
3. Inspect repository instructions and enough surrounding code to understand
   changed contracts, callers, tests, and data flow. Do not review a diff in
   isolation when its correctness depends on unchanged code.
4. Detect the relevant languages, frameworks, and databases from changed files
   and project manifests. Load only the matching references listed below.
5. Load cross-cutting references only when the change or the user's requested
   focus makes them relevant.
6. Validate each candidate finding against repository evidence. Remove style
   preferences, speculative concerns, duplicates, and issues already prevented
   by existing validation or tests.
7. Return findings in severity order using
   [assets/pr-review-template.md](assets/pr-review-template.md). If no findings
   survive validation, say so and mention meaningful residual risks or testing
   gaps.

## Reference routing

### Languages and frameworks

- C# or .NET: [references/languages/csharp.md](references/languages/csharp.md).
  Also read [references/frameworks/aspnet-core.md](references/frameworks/aspnet-core.md)
  for ASP.NET Core changes.
- Java: [references/languages/java.md](references/languages/java.md). Also read
  [references/frameworks/spring-boot.md](references/frameworks/spring-boot.md)
  for Spring Boot changes.
- Go: [references/languages/go.md](references/languages/go.md).
- PHP: [references/languages/php.md](references/languages/php.md).
- Python: [references/languages/python.md](references/languages/python.md).

### Databases

- MySQL: [references/databases/mysql.md](references/databases/mysql.md).
- PostgreSQL: [references/databases/postgresql.md](references/databases/postgresql.md).
- MongoDB: [references/databases/mongodb.md](references/databases/mongodb.md).

### Cross-cutting concerns

- Architecture, SOLID, boundaries, and dependency direction:
  [references/cross-cutting/architecture.md](references/cross-cutting/architecture.md).
- Authentication, authorization, injection, secrets, and unsafe trust
  boundaries: [references/cross-cutting/security.md](references/cross-cutting/security.md).
- Query count, allocation, contention, I/O, and algorithmic cost:
  [references/cross-cutting/performance.md](references/cross-cutting/performance.md).
- Recurring correctness traps and edge cases:
  [references/cross-cutting/common-bugs.md](references/cross-cutting/common-bugs.md).
- Failure translation, retries, fallbacks, cleanup, or background reliability:
  [references/cross-cutting/error-handling.md](references/cross-cutting/error-handling.md).
- Tasks, threads, goroutines, executors, queues, locks, cancellation, or shared state:
  [references/cross-cutting/async-concurrency.md](references/cross-cutting/async-concurrency.md).
- ORM queries, N+1 access, transactions, lost updates, idempotency, or caching:
  [references/cross-cutting/data-access.md](references/cross-cutting/data-access.md).
- APIs, events, schemas, configuration, rolling deployments, or stored contracts:
  [references/cross-cutting/api-compatibility.md](references/cross-cutting/api-compatibility.md).
- Changed behavior, bug fixes, integration boundaries, or modified tests:
  [references/cross-cutting/testing.md](references/cross-cutting/testing.md).

Use [assets/review-checklist.md](assets/review-checklist.md) as a final coverage
check, not as a reason to invent findings.

## Review constraints

- Findings must identify an observable failure mode, affected inputs or runtime
  conditions, and a precise code location.
- Prefer a small number of high-confidence findings over exhaustive commentary.
- Treat formatting, naming, and lint issues as out of scope unless they hide a
  defect or violate an explicit repository standard.
- Account for version-specific behavior. Infer versions from manifests or state
  uncertainty instead of assuming the newest runtime.
- Never claim a test, command, exploit, or benchmark was run unless it was.
- Treat the English headings in output templates as structural examples and
  translate them to the resolved response language.
