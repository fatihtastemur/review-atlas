# Security review

Follow data from untrusted input to privileged action or sensitive output. A
security finding must identify the trust boundary, missing control, and plausible
impact.

## Access control

- Authentication does not imply authorization. Verify action, resource, tenant,
  and ownership checks at a trusted server-side boundary.
- Ensure batch operations and indirect object references enforce the same policy
  as single-resource endpoints.
- Treat admin flags, roles, tenant IDs, prices, and ownership fields from clients
  as untrusted.

## Injection and unsafe interpretation

- Parameterize SQL and database filters; allow-list identifiers that cannot be bound.
- Avoid building shell commands, paths, templates, regular expressions, or URLs
  directly from user-controlled values.
- Validate archive extraction paths, redirects, webhook targets, and server-side
  fetches against traversal and SSRF.
- Encode output for its destination; input validation alone does not prevent XSS.

## Secrets and sensitive data

- Do not commit credentials or expose them in logs, URLs, traces, exceptions, or
  client-visible configuration.
- Use constant-time comparison and established libraries for cryptographic checks.
- Verify token signature, issuer, audience, expiry, algorithm, and key rotation.
- Minimize returned fields and redact personal or regulated data by default.

## State-changing operations

- Check CSRF protection when browser credentials are sent automatically.
- Validate webhook authenticity and replay resistance before processing effects.
- Make retries idempotent or detect duplicate operations.
- Apply rate and size limits before expensive parsing, hashing, decompression, or I/O.

## Dependencies and configuration

Check newly introduced packages, unsafe deserialization modes, permissive CORS,
debug endpoints, default credentials, wildcard network exposure, and production
configuration that weakens secure defaults.

## Review by trust boundary

Map each untrusted source to its sensitive sink:

- HTTP, RPC, WebSocket, message, file, webhook, and job inputs;
- identities, claims, tenant context, and delegated permissions;
- database, template, command, filesystem, network, redirect, and deserialization sinks;
- logs, traces, metrics, caches, exports, and client responses.

A finding should show how controlled input reaches the sink and why validation,
encoding, authorization, sandboxing, or parameterization does not stop it.

## Authentication and session details

- Verify credentials against the intended scheme and audience.
- Prevent account enumeration where it materially increases attackability.
- Rate-limit login, reset, verification, and recovery flows without enabling easy denial of service.
- Rotate sessions after privilege changes and define logout/revocation behavior.
- Recovery paths must not be weaker than primary authentication.
- MFA enrollment, disablement, and recovery are privileged state changes.

## Authorization and tenancy

- Check object ownership after loading the canonical resource.
- Scope collection, export, search, and aggregate queries—not only single-item reads.
- Enforce tenant context at a boundary shared by HTTP, jobs, messages, and admin tools.
- Treat role and scope changes as concurrency-sensitive; stale tokens may retain access.
- Avoid confused-deputy behavior when a service acts with broader credentials than the caller.

## Injection and parsing

- Parameterization protects values, not arbitrary identifiers or query structure.
- Normalize and validate paths after decoding; defend archive extraction and symlink traversal.
- URL allow-lists must account for redirects, DNS resolution, alternate IP notation,
  credentials, ports, and private/link-local networks.
- Limit recursive, compressed, nested, regex, XML, JSON, and multipart inputs before parsing.
- Safe deserialization requires both a safe format and a restricted type/model contract.

## Cryptography and secrets

- Use established password hashing, authenticated encryption, signatures, and secure randomness.
- Nonces/IVs must satisfy the selected algorithm's uniqueness requirements.
- Key identifiers and rotation must support overlap without accepting unknown algorithms.
- Compare secrets using appropriate constant-time primitives after validating types and lengths.
- Secrets need least privilege, rotation, redaction, and revocation—not merely environment variables.

## Supply chain and deployment

- Review dependency provenance, lock-file changes, install scripts, generated artifacts,
  build actions, container bases, and permissions.
- Pin immutable CI actions or trusted release identities according to project policy.
- Do not run untrusted pull-request code with write tokens or production secrets.
- Confirm debug, documentation, metrics, profiling, and management endpoints are restricted.

## Security checklist

- [ ] Every privileged action has server-side resource authorization.
- [ ] Tenant isolation covers reads, writes, caches, jobs, and exports.
- [ ] Untrusted data is safe at its actual destination.
- [ ] Sessions, tokens, recovery, and cryptography use complete validation.
- [ ] Sensitive data is minimized and redacted from every output channel.
- [ ] Dependencies and CI execute with least privilege and trustworthy provenance.
