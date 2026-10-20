# Contributing to ReviewAtlas

Thank you for improving ReviewAtlas. Contributions should increase review accuracy,
reduce false positives, or make installation and execution safer.

## Development setup

```bash
git clone https://github.com/fatihtastemur/review-atlas.git
cd review-atlas
python3 -m unittest discover -s tests -v
./bin/review-atlas review --dry-run
```

Python 3.10 or newer is required. Runtime code should use the standard library
unless a dependency provides a clear, reviewed benefit.

## Content guidelines

- Write all source content and code comments in English.
- Add guidance only when it changes review decisions or helps validate a finding.
- Explain the triggering condition and impact of every bug pattern.
- Prefer version-aware rules over claims that assume the newest runtime.
- Include code examples when syntax or framework behavior is otherwise ambiguous.
- Mark example comments as `Risky`, `Safer`, or similarly descriptive; avoid shaming language.
- Keep language, framework, database, and cross-cutting guidance in the appropriate reference.
- Link new references from `SKILL.md` with a clear loading condition.
- Do not copy third-party documentation or large code examples. Respect source licenses
  and provide attribution when a contribution is derived from another project.

## False-positive standard

A review rule should help establish all of the following:

1. a concrete failure or vulnerability;
2. a realistic trigger;
3. meaningful impact;
4. a precise location or evidence path;
5. checks for framework, validation, test, or database protections that may prevent it.

Generic preferences and formatter-managed issues do not belong in defect guidance.

## Testing changes

- Add unit tests for CLI behavior and safety boundaries.
- Add content-integrity tests for generated or linked resources.
- For a new review rule, prefer a small good/bad fixture or a documented real failure mode.
- Run `git diff --check` before opening a pull request.

## Pull requests

Keep a pull request focused. Describe the problem, why the proposed rule or behavior
improves review quality, validation performed, compatibility impact, and any remaining
limitations. Changes that alter output severity should explain their false-positive risk.
