# SHAMIR Quick Start

SHAMIR can run in base mode with no local model, or in local RAG/LLM mode with Ollama.

## 1. Clone and install

```bash
git clone https://github.com/alexslama/oracle-biblico-pro.git
cd oracle-biblico-pro
bash setup.sh
source venv/bin/activate
```

The setup script installs the runtime dependencies from `requirements.txt` and creates the local working directories. It does **not** download a biblical corpus, fine-tune a model, or create cloud resources.

## 2. Run base mode

```bash
python3 app.py
```

Open:

```text
http://127.0.0.1:5000
```

Base mode is intentionally transparent: without local generation enabled, analysis layers return `not_generated` instead of pretending to have produced scholarly conclusions.

## 3. Enable the bundled RAG demo

Install/start Ollama, then pull an embedding model:

```bash
ollama pull nomic-embed-text
```

Build the ChromaDB index from the redistribution-safe demo corpus:

```bash
python3 scripts/build_rag.py
```

Enable retrieval:

```bash
export SHAMIR_ENABLE_RAG=1
python3 app.py
```

`data/demo_corpus.jsonl` contains only small SHAMIR-authored demonstration notes. It is not a scholarly corpus.

## 4. Enable local LLM generation

Pull a local chat model:

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

The pipeline will retrieve local sources, label them as `S1`, `S2`, etc., and instruct the local model to ground factual claims in that retrieved context.

## 5. Use your own corpus

Create a JSONL file with one document per line:

```json
{"text":"Your legally usable source text.","metadata":{"source":"Source description"}}
```

Build an index from it:

```bash
python3 scripts/build_rag.py --input path/to/your_corpus.jsonl
```

Use only material you are legally allowed to process and redistribute.

## 6. Run tests

For development:

```bash
pip install -r requirements-dev.txt
pytest -q
```

The same core tests run automatically through GitHub Actions on pull requests.

## Useful endpoints

- `GET /api/health` — service and local AI status
- `POST /api/analyze` — run a research question
- `GET /api/results` — retrieve the most recently persisted result

## Current limits

SHAMIR is experimental. Retrieval quality depends on the indexed corpus, local models can still hallucinate, source labels are not formal academic citations, and historical/linguistic/theological claims require independent verification.

For architecture, configuration variables, roadmap, and contribution guidance, see [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
