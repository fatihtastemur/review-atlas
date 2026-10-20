# PHP review

Infer the PHP version, framework, static-analysis level, and strict-types usage from
the project before recommending syntax or behavior.

## Types and comparisons

- Prefer strict comparisons where coercion can turn distinct inputs into the same value.
- Check nullable, union, intersection, and `mixed` values at external boundaries.
- Distinguish missing array keys from present null values intentionally.
- Avoid dynamic properties and magic behavior that hide misspellings or bypass invariants.

## Errors and resources

- Preserve exception causes and framework error contracts; do not convert failures
  to empty data or success responses silently.
- Close or release streams, file handles, locks, transactions, and external clients on every path.
- Ensure shutdown or destructor behavior is not required for correctness.

## Security

- Parameterize PDO or ORM queries, including dynamic filters and ordering through allow-lists.
- Escape output for HTML, attributes, JavaScript, URLs, or headers at the output boundary.
- Validate uploads by content and size, generate server-side names, and keep them outside executable roots.
- Review deserialization, file inclusion, command execution, path traversal, session fixation, and mass assignment.

## Runtime behavior

- Watch truthiness checks that confuse `0`, `"0"`, empty strings, false, and null.
- Verify date/time zones, numeric precision, array key coercion, and JSON error handling.
- Avoid per-item ORM lazy loads and unbounded collection hydration.

## Runtime and dependency discovery

Inspect `composer.json`, `composer.lock`, platform requirements, extensions,
autoloading, framework version, static-analysis configuration, and test setup.
Do not assume production has the local PHP version or extensions.

## High-signal bug patterns

### Loose comparisons collapse distinct inputs

```php
// Risky: several values can compare equal after coercion.
if ($providedToken == $storedToken) {
    authorize();
}

// Safer for secrets after validating both values are strings.
if (is_string($providedToken) && hash_equals($storedToken, $providedToken)) {
    authorize();
}
```

Check `in_array`, `array_search`, switch behavior, numeric strings, and falsy values
for the same coercion issue.

### User fields overwrite protected state

```php
// Risky when payload contains role, owner_id, price, or status.
$entity->fill($request->all());
```

Prefer explicit input DTOs or allow-lists and enforce authorization independently
of which fields are accepted.

## Types, errors, and state

- `strict_types` affects calls made from the declaring file; it is not global validation.
- Distinguish absent keys with `array_key_exists` when null is a valid value.
- Check union types, `never`, enums, readonly properties, covariance, and contravariance
  against the declared runtime version.
- Avoid catching `Throwable` unless both `Error` and `Exception` have an intentional policy.
- Static state persists longer under workers and application servers than under classic request lifecycles.
- Generators may keep database cursors, transactions, or file handles open until exhausted.

## Web and security checks

- Validate CSRF for cookie-authenticated state changes and rotate session IDs after authentication.
- Configure cookies with appropriate Secure, HttpOnly, SameSite, path, and domain scope.
- Escape at the output context and review raw template directives carefully.
- Validate uploaded content, size, extension, storage path, and generated filename.
- Avoid `unserialize` on untrusted data and dynamic `include`, `eval`, shell, or filesystem paths.
- Review URL validation for SSRF, redirects, DNS rebinding assumptions, and private network access.

## Database and performance

- Ensure PDO emulated prepares and driver behavior match the threat model and data types.
- Check ORM hydration, lazy loading, query listeners, global scopes, soft deletes, and tenant filters.
- Bulk updates may bypass events, validation, casts, timestamps, or audit hooks.
- Transactions need rollback on every exceptional path and retry protection for deadlocks.
- Long-lived workers must release connections, streams, and per-request state.

## Testing expectations

- Use unit tests for pure services and integration tests for routing, middleware,
  validation, ORM mappings, transactions, templates, and authorization.
- Mutation or static analysis can expose tests that only execute code without checking behavior.
- Test numeric strings, zero, empty values, null, missing keys, Unicode, and timezone boundaries.
- Verify duplicate requests, retries, and queue redelivery for state-changing handlers.

## PHP review checklist

- [ ] Composer platform requirements match production.
- [ ] Comparisons and array-key checks preserve distinct domain values.
- [ ] Input mapping cannot overwrite protected state.
- [ ] Templates, queries, files, commands, and URLs handle untrusted data safely.
- [ ] ORM access is bounded and transaction behavior is explicit.
- [ ] Long-lived worker state and resources are reset between jobs.
