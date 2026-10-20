# Pull request review template

Use this template as an output shape, not as a requirement to fill every section.
Omit empty optional sections. Never create findings merely to populate the template.
Translate user-facing headings and prose into the user's resolved response
language. Keep code identifiers, paths, commands, and quoted diagnostics unchanged.

## Review context

- **Target:** PR, branch, commit range, working tree, or selected paths
- **Intent:** The behavior the change is meant to introduce or preserve
- **Primary risks:** Contracts, data, security, concurrency, rollout, or performance
- **Technology detected:** Relevant languages, frameworks, runtimes, and databases

## Findings

### [Severity] Short imperative title

- **Location:** `path/to/file.ext:line`
- **Impact:** Describe the user, system, security, or data consequence.
- **Evidence:** Explain what the changed code does and why surrounding code does not prevent the issue.
- **Trigger:** Give the smallest realistic input, state, timing, or deployment condition that exposes it.
- **Direction:** Describe the required outcome without prescribing an unnecessary rewrite.
- **Confidence:** High, medium, or low; lower confidence belongs in an open question
  unless the potential impact is important enough to surface.

Repeat only for validated findings, ordered from highest to lowest severity.

### Example

```text
[High] Preserve tenant scope in the batch update

Location: src/orders/update-orders.cs:84

The new update filters by order ID but no longer includes the authenticated tenant.
An authenticated user who can guess another tenant's order ID can therefore update
that record. The single-order path still applies the tenant predicate, so the batch
endpoint creates a concrete authorization bypass. Include the tenant in the update
predicate and verify the affected-row count before returning success.
```

Do not use an example as evidence. Every real finding must be derived from the reviewed code.

## Open questions / assumptions

Include only questions that could change the verdict or severity. State the evidence
that is missing and what answer would resolve the question.

## Suggestions

Put optional design, readability, documentation, or optimization improvements here.
Do not assign defect severity to a preference.

## Verdict

Choose one:

- **Request changes:** At least one Critical or High finding blocks merge.
- **Comment:** Only Medium or Low findings remain.
- **Approve:** No actionable findings remain.

## Review notes

- **Scope:** State the diff, branch, commit, PR, or paths reviewed.
- **Validation:** List relevant commands or tests actually run.
- **Residual risk:** Note important behavior that could not be verified.
- **Tests not run:** State the command and reason when relevant.
- **False-positive controls:** Mention important protections that were confirmed,
  such as a shared authorization layer or database constraint.

## Compact review format

For small changes, use:

```text
Findings

[Medium] Short title
Location: path/to/file.ext:42

Concrete failure, trigger, impact, and direction.

Verdict: Comment
Validation: command actually run
Residual risk: anything important not verified
```

## No-findings format

```text
No actionable findings.

Scope: main...feature/order-validation
Validation: unit and integration tests passed
Residual risk: production query plans were not available, so index behavior was not verified
Verdict: Approve
```
