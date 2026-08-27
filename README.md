# SHAMIR — Local-First Biblical Research Toolkit

SHAMIR is an open-source research toolkit for experimenting with biblical-text analysis using local language models, Retrieval-Augmented Generation (RAG), explicit source context, and a transparent Flask API.

The project is designed to keep the research workflow inspectable: the local corpus, embedding model, vector store, prompts, retrieved passages, generated analysis, warnings, and saved output can all be examined by the user.

> **Project status:** active experimental software. SHAMIR now includes a real local RAG path using Ollama embeddings + ChromaDB and an optional Ollama generation path. It is not a scholarly authority, and the quality of its answers depends heavily on the quality and licensing of the corpus you index.

## Why SHAMIR exists

Many AI-assisted research tools hide retrieval, prompts, source selection, or model behavior behind hosted services. SHAMIR explores a local-first alternative that developers and researchers can inspect, modify, test, and improve.

The project focuses on:

- local LLM experimentation;
- source-aware retrieval and RAG;
- structured linguistic, numerical, historical, and theological analysis layers;
- explicit uncertainty and verification requirements;
- reproducible local research workflows;
- Apple Silicon-friendly development;
- open collaboration around evaluation and hallucination reduction.

## What is implemented now

### Web/API layer

- Flask web application;
- `POST /api/analyze` for research questions;
- `GET /api/results` for the last persisted result;
- `GET /api/health` with RAG/LLM status;
- request validation and configurable query-length limits;
- production-safer defaults (`debug` is off unless explicitly enabled).

### Retrieval layer

- persistent ChromaDB collection;
- local embeddings through Ollama;
- deterministic document IDs for repeatable upserts;
- JSONL ingestion with source metadata;
- cosine-similarity retrieval;
- source labels (`S1`, `S2`, ...) propagated into the analysis context.

### Generation layer

- optional local generation through Ollama;
- four analysis layers: linguistic, numerical, historical, theological;
- integrated synthesis step;
- prompts that require evidence-conscious behavior and source labels;
- transparent `not_generated` responses when local generation is disabled.

### Quality layer

- pytest coverage for core pipeline behavior and API validation;
- GitHub Actions CI on pull requests and pushes to `main`;
- explicit warnings when retrieval fails;
- structured JSON output for downstream evaluation.

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
               +--> 4 analysis layers
               +--> integrated synthesis

Result -> JSON response + outputs/analysis_results.json
```

## Tech stack

- Python 3.12+
- Flask + Flask-CORS
- Ollama
- ChromaDB
- pytest
- HTML5 / CSS3 / JavaScript

The repository still contains additional experimental scripts and dependencies that may be simplified as the project is modularized.

## Quick start — base mode

Base mode requires no running local model and no vector database. The API starts and returns transparent placeholders for generation-dependent layers.

```bash
git clone https://github.com/alexslama/oracle-biblico-pro.git
cd oracle-biblico-pro

python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

On Windows, activate the virtual environment with the appropriate command for your shell.

Open:

```text
http://127.0.0.1:5000
```

## Enable real local RAG

SHAMIR does **not** bundle a scholarly or copyrighted biblical corpus. You are responsible for using texts you are legally allowed to index and redistribute.

Prepare a JSONL file where each line contains at least a `text` field:

```json
{"text":"A source passage or research note.","metadata":{"source":"Example source","license":"Your license information"}}
```

Start Ollama and install an embedding model, for example:

```bash
ollama pull nomic-embed-text
```

Build the persistent ChromaDB index:

```bash
python scripts/build_rag.py \
  --input data/processed/training_data.jsonl \
  --persist-dir data/vector_db \
  --collection shamir_sources \
  --embedding-model nomic-embed-text
```

Enable retrieval before starting the application:

```bash
export SHAMIR_ENABLE_RAG=1
python3 app.py
```

## Enable local LLM analysis

Install a local chat model in Ollama, for example:

```bash
ollama pull llama3.1
```

Then enable both retrieval and generation:

```bash
export SHAMIR_ENABLE_RAG=1
export SHAMIR_ENABLE_LLM=1
export SHAMIR_LLM_MODEL=llama3.1
python3 app.py
```

When generation is enabled, SHAMIR instructs the local model to ground factual claims in the retrieved context and refer to source labels such as `[S1]`. These labels refer to chunks returned from **your local corpus**; they are not a substitute for a formal academic bibliography.

## Configuration

Copy `.env.example` as a reference for available settings. Environment variables include:

| Variable | Default | Purpose |
| --- | --- | --- |
| `SHAMIR_ENABLE_RAG` | `0` | Enable ChromaDB retrieval |
| `SHAMIR_ENABLE_LLM` | `0` | Enable local Ollama generation |
| `SHAMIR_VECTOR_DB` | `data/vector_db` | ChromaDB persistence path |
| `SHAMIR_COLLECTION` | `shamir_sources` | Collection name |
| `SHAMIR_EMBEDDING_MODEL` | `nomic-embed-text` | Ollama embedding model |
| `SHAMIR_LLM_MODEL` | `llama3.1` | Ollama chat model |
| `SHAMIR_TOP_K` | `5` | Maximum retrieved sources per query |
| `SHAMIR_MAX_QUERY_LENGTH` | `4000` | API input limit |

## API

### `GET /api/health`

Reports service version plus local pipeline configuration:

```json
{
  "status": "healthy",
  "service": "SHAMIR",
  "pipeline": {
    "rag_enabled": false,
    "generation_enabled": false
  }
}
```

### `POST /api/analyze`

Request:

```json
{
  "query": "What evidence supports this interpretation?"
}
```

Response fields include:

- `mode`: whether RAG and local generation were enabled;
- `sources`: retrieved local evidence with metadata and similarity distance;
- `analysis_layers`: structured layer outputs;
- `synthesis`: integrated result;
- `warnings`: retrieval/configuration problems that should not be hidden.

### `GET /api/results`

Returns the last analysis persisted to `outputs/analysis_results.json` when available.

## Tests

Run the local unit tests with:

```bash
pytest -q
```

The GitHub Actions workflow intentionally tests the core Flask/pipeline behavior without requiring an Ollama service, so pull requests can be validated reproducibly. Integration tests against real local models and vector stores remain a roadmap item.

## Repository structure

```text
oracle-biblico-pro/
├── .github/workflows/tests.yml
├── .env.example
├── app.py
├── scripts/
│   ├── analysis_pipeline.py
│   ├── build_rag.py
│   ├── rag_store.py
│   ├── collect_data.py
│   ├── finetune_llama.py
│   ├── generate_divine_audio.py
│   └── prepare_training_data.py
├── tests/
│   ├── test_analysis_pipeline.py
│   └── test_app.py
├── templates/
├── static/
├── requirements.txt
├── CONTRIBUTING.md
└── LICENSE
```

## Roadmap

### Near term

- [x] Replace simulated embedding/index code with real Ollama + ChromaDB retrieval
- [x] Connect retrieved sources to the analysis pipeline
- [x] Add source labels and retrieval metadata
- [x] Add automated tests for API and pipeline behavior
- [x] Add GitHub Actions CI
- [ ] Add a redistribution-safe sample research corpus
- [ ] Add integration tests for live Ollama + ChromaDB
- [ ] Add automated citation-format validation
- [ ] Add retrieval-quality evaluation fixtures

### Mid term

- [ ] Modularize LLM and vector-store providers behind stable interfaces
- [ ] Add hallucination and groundedness evaluation
- [ ] Add token/context budgeting for large retrieved passages
- [ ] Improve Hebrew / Greek / Aramaic processing with verifiable linguistic resources
- [ ] Add benchmark questions with expected evidence sets
- [ ] Split production dependencies from optional research dependencies

### Long term

- [ ] Package reusable SHAMIR components as an installable Python library
- [ ] Support contributor-provided analysis modules
- [ ] Add auditable research sessions with stable source manifests
- [ ] Publish documented evaluation results and regression benchmarks

## Research, theology, and accuracy disclaimer

SHAMIR is experimental software. Outputs about history, linguistics, archaeology, theology, gematria, manuscripts, dates, or textual interpretation require independent verification. The system is designed to make uncertainty and evidence more visible, not to replace primary sources, qualified scholarship, or critical review.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Especially useful contribution areas include retrieval, embeddings, evaluation, tests, documentation, local-model support, source attribution, dependency cleanup, and reproducibility.

## License

SHAMIR is released under the [MIT License](LICENSE).

## Maintainer

**Alex Slama**

Independent builder working with open-source AI, local models, RAG, automation, and reproducible AI-assisted research workflows.
