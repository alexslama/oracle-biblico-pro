# Contributing to SHAMIR

Thank you for your interest in contributing to SHAMIR.

SHAMIR is an experimental open-source project exploring local-first Retrieval-Augmented Generation, local language models, transparent source context, and reproducible AI-assisted research workflows.

## Good contribution areas

Contributions are especially welcome in:

- retrieval quality and corpus ingestion;
- Ollama/model-provider abstractions;
- ChromaDB/vector-store abstractions;
- groundedness and hallucination evaluation;
- source attribution and citation validation;
- tests and CI;
- dependency/security improvements;
- documentation and examples;
- Hebrew / Greek / Aramaic processing backed by verifiable resources;
- accessibility and web-interface improvements.

## Development setup

```bash
git clone https://github.com/alexslama/oracle-biblico-pro.git
cd oracle-biblico-pro
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

Run the web app with:

```bash
python3 app.py
```

The default server is `http://127.0.0.1:5000`.

## Optional local AI stack

Unit tests do not require Ollama. For live RAG experiments, install/start Ollama and follow [QUICK_START.md](QUICK_START.md).

Do not make the default test suite depend on downloading large models or external proprietary services. Integration tests that need local models should be clearly separated and documented.

## Pull requests

Please:

- keep changes focused;
- explain the problem before the implementation;
- add or update tests when behavior changes;
- update documentation when setup or API behavior changes;
- preserve transparent failure states instead of hiding errors;
- avoid unsupported scientific, medical, historical, linguistic, or theological claims;
- avoid committing credentials, `.env` files, private corpora, model weights, generated vector stores, or sensitive outputs.

A useful PR description includes:

- what changed;
- why it changed;
- how it was tested;
- known limitations;
- follow-up work, if any.

## Corpus and licensing rules

Only add corpus material that the project is legally allowed to redistribute. Do not commit copyrighted translations, commentaries, academic databases, scraped paywalled sources, or private user material without explicit rights.

When adding a reusable corpus or benchmark, document:

- provenance;
- license/redistribution terms;
- transformation steps;
- intended evaluation use;
- known limitations or bias.

## Research-quality principles

SHAMIR should distinguish:

- retrieved evidence from generated interpretation;
- verifiable claims from uncertainty;
- theological tradition from historical evidence;
- numerical/gematria interpretation from empirical fact;
- demo fixtures from scholarly corpora;
- implemented behavior from roadmap ideas.

A feature should not be described as implemented until the code path genuinely performs it.

## Security

Review [SECURITY.md](SECURITY.md). Local model output is untrusted, and local corpora may contain sensitive information. Avoid patterns that execute model output or expose local files without validation.

## Issues

For bugs, include:

- operating system;
- Python version;
- steps to reproduce;
- expected behavior;
- actual behavior;
- relevant logs with secrets removed.

For feature requests, describe the user/research problem first and the proposed implementation second.

## License

By contributing to this repository, you agree that your contributions will be licensed under the MIT License.
