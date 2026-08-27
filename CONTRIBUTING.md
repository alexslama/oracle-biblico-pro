# Contributing to SHAMIR

Thank you for your interest in contributing to SHAMIR.

SHAMIR is an early-stage open-source project exploring structured biblical-text analysis, local language models, and Retrieval-Augmented Generation (RAG). The project is still evolving, so contributions that improve correctness, reproducibility, testing, documentation, and modularity are especially welcome.

## Ways to contribute

You can help by:

- fixing bugs or dependency issues;
- improving documentation and examples;
- adding or improving tests;
- improving the analysis pipeline;
- replacing prototype or simulated RAG components with real retrieval and embedding implementations;
- improving source attribution and evaluation;
- improving support for local models and Apple Silicon;
- proposing clearer APIs or reusable components.

## Development setup

1. Fork or clone the repository.
2. Create a virtual environment:

```bash
python3.12 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the web application:

```bash
python3 app.py
```

The application is served locally at `http://localhost:5000` by default.

## Pull requests

Before opening a pull request:

- keep the change focused;
- explain what problem it solves;
- include tests when changing behavior where practical;
- update documentation when behavior or setup changes;
- avoid committing credentials, private datasets, generated model files, or secrets.

A good pull request description should include:

- what changed;
- why it changed;
- how it was tested;
- any known limitations or follow-up work.

## Issues

When reporting a bug, include your operating system, Python version, steps to reproduce, expected behavior, actual behavior, and any relevant error output.

For feature requests, describe the use case first and the proposed implementation second.

## Project principles

SHAMIR aims to be transparent about what is implemented versus experimental. Claims about historical, linguistic, theological, or numerical analysis should be treated as research output requiring verification, not as authoritative truth.

## License

By contributing to this repository, you agree that your contributions will be licensed under the MIT License.
