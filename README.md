# SHAMIR — Local-First Biblical Research Toolkit

SHAMIR is an open-source experimental toolkit for source-aware biblical-text research using local language models, Retrieval-Augmented Generation (RAG), and a transparent Flask API.

The project is designed so users can inspect the full workflow: local corpus, embeddings, vector store, retrieved passages, prompts, generated analysis, warnings, and persisted JSON output.

> **Status:** active experimental software. SHAMIR includes a real local RAG path with Ollama embeddings + ChromaDB and optional local generation with Ollama. It is not a scholarly authority, and every historical, linguistic, archaeological, theological, or numerical claim should be independently verified.

## Why SHAMIR exists

Many AI research tools hide retrieval, prompts, source selection, or model behavior behind hosted services. SHAMIR explores a local-first alternative that developers and researchers can inspect, modify, test, and improve.

The project focuses on:

- local LLM experimentation;
- transparent source-aware retrieval;
- structured research layers;
- explicit uncertainty and verification requirements;
- reproducible local workflows;
- Apple Silicon-friendly development;
- open collaboration around evaluation and hallucination reduction.

## Current capabilities

### Flask API

- `POST /api/analyze` — analyze a research question;
- `GET /api/results` — return the latest persisted result;
- `GET /api/health` — report service, RAG, LLM, and index status;
- request validation and configurable query limits;
- debug mode disabled by default;
- generic server errors so internal exceptions are not leaked to clients.

### Local RAG

- persistent ChromaDB collection;
- embeddings through a locally running Ollama service;
- deterministic document IDs for repeatable upserts;
- JSONL corpus ingestion;
- source metadata preservation;
- cosine-similarity retrieval;
- source labels (`S1`, `S2`, ...) propagated into the analysis context.

### Local generation

- optional Ollama chat generation;
- linguistic, numerical, historical, and theological analysis layers;
- integrated synthesis;
- prompts requiring evidence-conscious behavior and source labels;
- transparent `not_generated` / `generation_failed` states when local generation is disabled or unavailable.

### Quality and project health

- pytest tests for pipeline, API, and corpus ingestion;
- GitHub Actions CI on pull requests and pushes to `main`;
- MIT license;
- contribution guidelines;
- security reporting policy;
- `.gitignore` for local vector stores, models, outputs, virtual environments, and secrets;
- redistribution-safe SHAMIR-authored demo corpus.

## Architecture

```text
User / Web UI
     |
     v
 Flask API
     |
     v
BiblicalAnalysisPipeline
     |
     +--> ChromaRAGStore ----> Ollama embeddings
     |         |
     |         +--> retrieved local sources [S1..Sn]
     |
     +--> OllamaGenerator (optional)
               |
               +--> linguistic analysis
               +--> numerical analysis
               +--> historical analysis
               +--> theological analysis
               +--> integrated synthesis

Result -> JSON response + outputs/analysis_results.json
```

## Tech stack

- Python 3.12+
- Flask + Flask-CORS
- Ollama
- ChromaDB
- python-dotenv
- pytest
- HTML5 / CSS3 / JavaScript

## Quick start

```bash
git clone https://github.com/alexslama/oracle-biblico-pro.git
cd oracle-biblico-pro
bash setup.sh
source venv/bin/activate
python3 app.py
```

Open:

```text
http://127.0.0.1:5000
```

Base mode starts without requiring Ollama. Generation-dependent layers return transparent placeholders instead of pretending that model-backed analysis happened.

For a shorter walkthrough, see [QUICK_START.md](QUICK_START.md).

## Run the bundled RAG demo

Install/start Ollama and pull an embedding model:

```bash
ollama pull nomic-embed-text
```

Build the demo index:

```bash
python3 scripts/build_rag.py
```

The default input is:

```text
data/demo_corpus.jsonl
```

This file contains only small SHAMIR-authored demonstration notes. It is **not** a scholarly or biblical-text corpus.

Enable retrieval:

```bash
export SHAMIR_ENABLE_RAG=1
python3 app.py
```

## Enable local LLM analysis

Pull a local model, for example:

```bash
ollama pull llama3.1
```

Then run:

```bash
export SHAMIR_ENABLE_RAG=1
export SHAMIR_ENABLE_LLM=1
export SHAMIR_LLM_MODEL=llama3.1
python3 app.py
```

When generation is enabled, SHAMIR instructs the model to ground factual claims in the retrieved local context and reference labels such as `[S1]`. These labels refer to retrieved chunks from **your local corpus** and are not a substitute for formal academic citations.

## Use your own corpus

Create a JSONL file with one document per line:

```json
{"text":"Your legally usable source text.","metadata":{"source":"Source description"}}
```

Index it with:

```bash
python3 scripts/build_rag.py --input path/to/your_corpus.jsonl
```

Use only material you are legally allowed to process. SHAMIR does not bundle copyrighted biblical translations, commentaries, or scholarly databases.

## Configuration

Environment variables can be exported manually or placed in a local `.env` file. See [.env.example](.env.example).

| Variable | Default | Purpose |
| --- | --- | --- |
| `SHAMIR_ENABLE_RAG` | `0` | Enable ChromaDB retrieval |
| `SHAMIR_ENABLE_LLM` | `0` | Enable local Ollama generation |
| `SHAMIR_VECTOR_DB` | `data/vector_db` | ChromaDB persistence path |
| `SHAMIR_COLLECTION` | `shamir_sources` | ChromaDB collection name |
| `SHAMIR_EMBEDDING_MODEL` | `nomic-embed-text` | Ollama embedding model |
| `SHAMIR_LLM_MODEL` | `llama3.1` | Ollama chat model |
| `SHAMIR_TOP_K` | `5` | Maximum retrieved sources per query |
| `SHAMIR_MAX_QUERY_LENGTH` | `4000` | API query-length limit |
| `SHAMIR_HOST` | `127.0.0.1` | Flask bind host |
| `SHAMIR_PORT` | `5000` | Flask port |

## Tests

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run:

```bash
pytest -q
```

GitHub Actions runs the same core test suite automatically. The CI does not require a live Ollama server; integration tests against real local models/vector stores remain a roadmap item.

## Repository structure

```text
oracle-biblico-pro/
├── .github/workflows/tests.yml
├── .env.example
├── .gitignore
├── app.py
├── data/
│   └── demo_corpus.jsonl
├── scripts/
│   ├── __init__.py
│   ├── analysis_pipeline.py
│   ├── build_rag.py
│   ├── rag_store.py
│   ├── collect_data.py
│   ├── prepare_training_data.py
│   ├── finetune_llama.py
│   └── generate_divine_audio.py
├── tests/
│   ├── test_analysis_pipeline.py
│   ├── test_app.py
│   └── test_rag_store.py
├── requirements.txt
├── requirements-dev.txt
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

## Legacy experimental helpers

Some scripts retain historical filenames for compatibility, but their behavior is now deliberately explicit:

- `collect_data.py` creates **demo metadata only**; it does not download biblical texts;
- `prepare_training_data.py` creates a **development metadata fixture**; it does not create a real fine-tuning corpus;
- `finetune_llama.py` writes a **configuration plan only**; it does not train a model;
- `generate_divine_audio.py` creates simple sine-wave audio experiments and makes **no medical or therapeutic claims**.

This distinction is intentional: SHAMIR should state what it actually does, not what a future version might do.

## Roadmap

### Completed in the current open-source hardening work

- [x] MIT licensing
- [x] contribution guidelines
- [x] real Ollama + ChromaDB indexing path
- [x] retrieval connected to the analysis pipeline
- [x] local Ollama generation path
- [x] source labels and retrieval metadata
- [x] API validation and safer server defaults
- [x] automated unit tests
- [x] GitHub Actions CI
- [x] redistribution-safe demo corpus
- [x] dependency cleanup
- [x] security policy and local-secret ignores
- [x] removal of unsupported therapeutic/audio claims
- [x] transparent labeling of legacy scaffolds

### Next

- [ ] live Ollama + ChromaDB integration tests
- [ ] automated citation-format validation
- [ ] groundedness/hallucination evaluation
- [ ] retrieval-quality benchmark fixtures
- [ ] context/token budgeting
- [ ] verifiable Hebrew / Greek / Aramaic resources
- [ ] stable provider interfaces for alternate vector stores/models
- [ ] installable Python package
- [ ] auditable research-session manifests

## Research and accuracy disclaimer

SHAMIR is experimental software. Outputs about history, linguistics, archaeology, theology, manuscripts, dates, gematria, or textual interpretation require independent verification. Retrieval improves traceability but does not prove that a generated conclusion is correct.

## Security

See [SECURITY.md](SECURITY.md). Local corpora may contain sensitive material, so users should avoid indexing secrets, credentials, private personal data, or content they are not authorized to process.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Especially useful areas include retrieval, embeddings, evaluation, tests, documentation, local-model support, source attribution, dependency cleanup, and reproducibility.

## License

SHAMIR is released under the [MIT License](LICENSE).

## Maintainer

**Alex Slama**

Independent builder working with open-source AI, local models, RAG, automation, and reproducible AI-assisted research workflows.
