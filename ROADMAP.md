# SHAMIR Roadmap

This roadmap describes intended engineering work, not promises of delivery dates. Items move to complete only after code, tests, and documentation exist in the public repository.

## v0.3 — Reusable local research toolkit

- [x] Installable Python package and `shamir` CLI
- [x] Persistent ChromaDB retrieval with Ollama embeddings
- [x] Optional Ollama generation with transparent failure states
- [x] Flask API and CLI entry points
- [x] Deterministic citation-label integrity evaluator
- [x] Automated tests and GitHub Actions CI
- [x] Corpus provenance/licensing guidance
- [ ] Fixed benchmark question set and benchmark runner
- [ ] Machine-readable run manifest with model/environment metadata

## v0.4 — Retrieval and citation evaluation

- [ ] Labeled retrieval benchmark with expected source IDs
- [ ] Recall@k and MRR metrics for retrieval
- [ ] Claim segmentation for generated answers
- [ ] Claim-to-source support evaluation with documented limitations
- [ ] Citation completeness metric
- [ ] Regression reports across model/provider versions
- [ ] Reproducible benchmark artifacts published with releases

## v0.5 — Provider-independent architecture

- [ ] Formal embedding provider protocol
- [ ] Formal retriever/vector-store protocol
- [ ] Formal generator protocol
- [ ] Configuration objects instead of environment-only settings
- [ ] Optional providers beyond Ollama/Chroma without changing pipeline semantics
- [ ] Structured logging and trace IDs

## v0.6 — Research corpus tooling

- [ ] Corpus validation command
- [ ] Provenance/schema validation
- [ ] Duplicate and near-duplicate detection
- [ ] Chunking strategies with stable source locators
- [ ] Public-domain / permissively licensed example corpus workflow
- [ ] Corpus manifest and hashing tools

## v0.7 — Scholarly review workflow

- [ ] Human review rubric for historical claims
- [ ] Human review rubric for linguistic claims
- [ ] Explicit separation of evidence, interpretation, and tradition
- [ ] Review annotations stored alongside generated results
- [ ] Exportable research bundles containing question, sources, model metadata, output, and evaluation

## v1.0 — Stable open-source library

A 1.0 release should require:

- stable documented Python APIs;
- provider interfaces with compatibility tests;
- reproducible benchmark suite;
- strong corpus provenance tooling;
- citation and retrieval evaluation;
- security and contribution policies;
- versioned releases and changelog;
- evidence of external use or contribution before making ecosystem-impact claims.

## Project principle

SHAMIR should never claim adoption, accuracy, scholarly authority, or ecosystem importance that the public evidence does not support. Technical credibility and external adoption must be earned separately.
