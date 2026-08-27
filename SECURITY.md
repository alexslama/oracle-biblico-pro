# Security Policy

SHAMIR is experimental local-first software. Security reports are welcome, especially for issues involving remote code execution, path traversal, unsafe file handling, dependency compromise, prompt/data exfiltration, or unintended exposure of local research material.

## Supported version

Security fixes currently target the latest `main` branch.

## Reporting a vulnerability

Please do **not** publish a working exploit or sensitive details in a public issue before the maintainer has had a reasonable opportunity to investigate.

For a report, include:

- the affected file or component;
- steps to reproduce;
- expected and actual behavior;
- impact and prerequisites;
- suggested remediation, if known.

If private security reporting is enabled for this repository, prefer GitHub's private vulnerability reporting flow. Otherwise, open a minimal public issue asking for a private contact channel without including exploit details.

## Local-data assumptions

SHAMIR may process user-supplied corpora and persist a local ChromaDB index. Users should avoid placing secrets, credentials, private personal data, or material they are not authorized to process in the indexed corpus.

## Model-output safety

Local LLM output is untrusted data. Applications built on SHAMIR should not execute generated commands, code, URLs, or file paths without independent validation.
