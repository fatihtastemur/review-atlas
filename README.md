# ReviewAtlas

A CLI-first, polyglot code review skill and standards library for AI coding agents.

ReviewAtlas gives Claude Code a focused, evidence-driven review workflow with
progressively loaded guidance for languages, frameworks, architecture,
security, performance, and databases.

## Coverage

| Area | Coverage |
| --- | --- |
| Languages | C#/.NET, Java, Go, PHP, Python |
| Frameworks | ASP.NET Core, EF Core, Spring Boot, Spring Security, JPA/Hibernate |
| Databases | MySQL, PostgreSQL, MongoDB |
| Architecture | SOLID, Clean Architecture, dependency direction, distributed boundaries |
| Reliability | Error handling, retries, idempotency, async/concurrency, transactions |
| Security | Authentication, authorization, tenant isolation, injection, secrets, supply chain |
| Performance | Query count, plans, N+1, allocations, concurrency, caching, measurement |
| Compatibility | APIs, events, schemas, rolling deployments, stored data |
| Testing | Unit, integration, contract, concurrency, and regression-test quality |

## Status

ReviewAtlas is in early development. The initial release targets local Git
changes and branches in C#/.NET, Java/Spring Boot, Go, PHP, and Python projects.

## Installation

ReviewAtlas supports two installation methods:

- **Claude account package:** appears under **Settings → Skills → Yours** and
  can be synchronized to supported Claude sessions.
- **Local Code installation:** loads directly from `~/.claude/skills/` and is
  intended for local repositories in Claude Code.

### Install from Claude Desktop

1. Download `review-atlas.skill` from the
   [latest GitHub Release](https://github.com/fatihtastemur/review-atlas/releases/latest).
2. Open Claude Desktop and go to **Settings → Skills**.
3. Select **Add** and choose the skill upload option.
4. Select the downloaded `review-atlas.skill` file.
5. Confirm that ReviewAtlas appears under **Yours**.

Account-installed skills are managed separately from local filesystem skills.
For code review, open a Code session with access to the target Git repository.

### Install for Local Code

#### 1. Check the requirements

- macOS or Linux; Windows should use WSL until native installation is verified
- Python 3.10 or newer
- Git
- Claude Desktop with the Code tab

Verify the required commands:

```bash
python3 --version
git --version
```

#### 2. Clone ReviewAtlas

```bash
git clone https://github.com/fatihtastemur/review-atlas.git
cd review-atlas
```

#### 3. Install the Claude Code Desktop skill

```bash
./bin/review-atlas install
```

This creates `~/.claude/skills/review-atlas`, which makes `/review-atlas`
available in local Claude Code sessions inside Claude Desktop.

ReviewAtlas uses symbolic links, so pulling repository updates also updates the
installed skill.

#### 4. Verify the Desktop installation

```bash
./bin/review-atlas doctor
```

The `claude` check accepts either Claude Code CLI or Claude Desktop. Each check
should report `ok`.

#### Optional: install the terminal command

Desktop users do not need the ReviewAtlas terminal command. Install it only if
you also want to start reviews from a shell:

```bash
./bin/review-atlas install --command
```

This additionally creates `~/.local/bin/review-atlas`.

Check whether the command is available:

```bash
command -v review-atlas
```

If it is not found, add `~/.local/bin` to your shell configuration.

For Zsh:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

For Bash:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Project-scoped installation

To make the skill available only in one project, omit the user-level install and
run the following commands from the cloned ReviewAtlas repository:

```bash
./bin/review-atlas install --scope project --project /path/to/project
./bin/review-atlas doctor --scope project --project /path/to/project
```

ReviewAtlas refuses to replace an existing skill or install recursively inside
its own source checkout.

## Run a review in Claude Code

### 1. Open a local Code session

Open Claude Desktop, select the **Code** tab, choose the **Local** environment,
and open the project directory. Check out the development branch from the branch
selector or the integrated terminal.

### 2. Start ReviewAtlas

Inside Claude Code, enter only:

```text
/review-atlas
```

No explanatory prompt is required.

When the current branch is a feature branch, ReviewAtlas treats `current` as the
selected target. It detects the likely base and reviews only changes introduced
by the feature branch, together with staged, unstaged, and untracked changes.

### Long-lived branch helper

ReviewAtlas treats `main`, `master`, `test`, `stage`, `dev`, and `develop` as
long-lived branches. Running `/review-atlas` on one of these branches does not
start a potentially project-wide review. It shows this helper first:

```text
Choose a review target:
- branch <name>  Review changes introduced by a branch
- staged         Review only staged changes
- commit <sha>   Review one commit
- pr <number>    Review a pull request
- paths <paths>  Review selected files or directories

Which branch or target should I review?
```

Respond with a target such as:

```text
branch feature/orders
```

ReviewAtlas then determines that branch's likely base and reviews only the
changes introduced by the selected branch.

### Output language

ReviewAtlas follows the language used in the conversation. To set a persistent
default for all repositories, configure a language code once:

```bash
git config --global review-atlas.language tr
```

Use a repository-specific value by omitting `--global`. An explicit language
request in the conversation always takes precedence.

### Skill does not appear in Claude Desktop

Personal skills under `~/.claude/skills/` are available in **Local Code**
sessions. They are not loaded from the local machine in Cowork or cloud
sessions. In Claude Desktop:

1. Open the project in the **Code** tab with the **Local** environment.
2. Enter `/reload-skills` in the prompt.
3. Enter `/skills`, or open **+ → Slash commands**, and search for
   `review-atlas`.
4. If it is still missing, fully quit Claude Desktop, reopen it, and create a
   new Local Code session.

Confirm the installation path from Terminal when troubleshooting:

```bash
ls -la ~/.claude/skills/review-atlas
./bin/review-atlas doctor
```

## Run a review from the terminal

Run the CLI from any Git repository:

```bash
review-atlas review
review-atlas review --staged
review-atlas review --branch feature/orders
review-atlas review --base main --focus "security and database performance"
review-atlas review --pr 42
review-atlas review --print
```

The normal command is `review-atlas review`. It follows the same feature-branch
and long-lived-branch behavior as `/review-atlas` in Claude Code.

If a repository uses a non-standard long-lived base branch, configure it once:

```bash
git config review-atlas.baseBranch develop
```

By default, the CLI starts an interactive Claude Code session. Use `--print`
for non-interactive output or `--dry-run` to inspect the generated prompt
without invoking Claude.

## Design principles

- Report concrete, actionable findings before summaries.
- Prioritize correctness, security, data integrity, and regressions over style.
- Load only the language, framework, database, and cross-cutting guides needed
  for the current change.
- Separate observed evidence from assumptions and unresolved questions.
- Do not modify reviewed code unless the user explicitly asks for fixes.

## Repository structure

```text
review-atlas/
├── .github/workflows/ci.yml
├── .github/workflows/release.yml
├── SKILL.md
├── CONTRIBUTING.md
├── SECURITY.md
├── assets/
│   ├── pr-review-template.md
│   └── review-checklist.md
├── bin/review-atlas
├── scripts/package_skill.py
├── references/
│   ├── cross-cutting/
│   ├── databases/
│   ├── frameworks/
│   ├── languages/
│   └── review-process.md
└── tests/
    ├── test_cli.py
    ├── test_content.py
    └── test_package.py
```

## Development

Run the built-in tests and validate the skill metadata:

```bash
python3 -m unittest discover -s tests -v
```

All runtime behavior uses the Python standard library. Development tests require
no third-party Python packages.

Build the Claude account upload package locally:

```bash
./bin/review-atlas package
```

The command creates `dist/review-atlas.skill`. The archive contains only
`SKILL.md`, `LICENSE`, `assets/`, and `references/`. It excludes repository,
test, CLI, and CI files.

Tags beginning with `v` run the test suite, build the `.skill` package, and
attach it to a GitHub Release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

## License

[MIT](LICENSE)
