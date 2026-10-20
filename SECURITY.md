# Security policy

## Reporting a vulnerability

Do not open a public issue for a vulnerability that could expose users, credentials,
source code, or local files. Use GitHub's private vulnerability reporting or private
security advisory feature for this repository.

Include:

- affected version or commit;
- installation and execution mode;
- reproduction steps;
- expected and observed behavior;
- realistic impact;
- suggested mitigation, if known.

Please avoid accessing data that does not belong to you, disrupting third-party
services, or publishing exploit details before a fix is available.

## Security model

ReviewAtlas installs local symbolic links and invokes an existing Claude Code CLI.
It does not request API keys, store credentials, or upload source code itself. The
selected AI coding agent and its configured providers determine where reviewed source
is processed.

ReviewAtlas refuses to overwrite existing installation paths and refuses recursive
project installation inside its own source checkout. Users should review repository
changes before running project scripts and should apply least-privilege agent permissions.

## Supported versions

Security fixes are applied to the latest release line. Until ReviewAtlas reaches a
stable release, users should expect breaking changes and update to the newest version.
