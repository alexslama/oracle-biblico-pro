# SHAMIR — Open-Source Biblical Analysis Research Toolkit

SHAMIR is an early-stage open-source research project for experimenting with structured biblical-text analysis, local language models, and Retrieval-Augmented Generation (RAG).

The project is designed around a local-first workflow: Python services, a web interface, structured analysis layers, data-preparation scripts, and experimental RAG components that can evolve into a reusable toolkit for researchers and developers.

> **Project status:** experimental / prototype. Some analysis and RAG components currently use deterministic or simulated outputs and are not yet connected to a production retrieval pipeline. The repository intentionally documents this distinction so contributors can clearly see what is implemented and what remains on the roadmap.

## Why this project exists

Many AI-assisted research tools depend on closed hosted services or hide their retrieval and analysis pipeline. SHAMIR explores a more transparent approach where developers can inspect, run, modify, and evaluate the full workflow locally.

The long-term goal is to provide reusable components for:

- local LLM experimentation;
- structured multi-layer text analysis;
- source-aware retrieval and RAG;
- evaluation and hallucination reduction;
- reproducible research workflows;
- Apple Silicon-friendly local deployment.

## Current architecture

The repository currently includes:

- a **Flask web application** with JSON API endpoints;
- a **five-layer analysis framework** covering linguistic, numerical, historical, theological, and integrated analysis;
- scripts for **data collection and preparation**;
- an experimental **RAG builder**;
- local-model and training experiments;
- setup/deployment tooling for macOS / Apple Silicon;
- HTML/CSS/JavaScript web UI.

### Important implementation note

The current `analysis_pipeline.py` is a structured prototype: it returns deterministic analysis structures rather than fully model-generated scholarly conclusions. The current `build_rag.py` also contains simulated embedding/index steps. Connecting these components to real embeddings, retrieval, source attribution, and evaluation is a primary roadmap item.

## Tech stack

- Python 3.12+
- Flask + Flask-CORS
- Ollama
- LangChain
- ChromaDB / Pinecone dependencies for retrieval experiments
- HTML5 / CSS3 / JavaScript
- pytest tooling

## Quick start

### Requirements

- Python 3.12+
- Git
- 8 GB+ RAM recommended for local-model experiments
- macOS, Linux, or Windows; Apple Silicon is a primary development target

### Install

```bash
git clone https://github.com/alexslama/oracle-biblico-pro.git
cd oracle-biblico-pro

python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

On Windows, activate the environment with the appropriate command for your shell.

Then open:

```text
http://localhost:5000
```

The repository also includes `DEPLOY_M1_MAC.sh` and `setup.sh` for local setup experiments.

## API

The Flask application currently exposes:

### `GET /api/health`

Returns a basic service health response.

### `POST /api/analyze`

Example request:

```json
{
  "query": "Example research question"
}
```

Returns the current structured five-layer analysis result.

### `GET /api/results`

Returns the latest saved analysis output when available.

## Repository structure

```text
oracle-biblico-pro/
├── app.py
├── scripts/
│   ├── analysis_pipeline.py
│   ├── build_rag.py
│   ├── collect_data.py
│   ├── finetune_llama.py
│   ├── generate_divine_audio.py
│   └── prepare_training_data.py
├── templates/
├── static/
├── QUICK_START.md
├── WEB_INTERFACE.md
├── requirements.txt
├── CONTRIBUTING.md
└── LICENSE
```

## Roadmap

### Near term

- [ ] Replace simulated embeddings with a real embedding provider
- [ ] Connect retrieval results to the analysis pipeline
- [ ] Add explicit source attribution and citation metadata
- [ ] Add automated tests for API and pipeline behavior
- [ ] Add CI with GitHub Actions
- [ ] Add reproducible sample datasets suitable for redistribution

### Mid term

- [ ] Modularize model and vector-store providers
- [ ] Add retrieval-quality and hallucination evaluation
- [ ] Create clearer public Python APIs for reuse by other projects
- [ ] Improve multilingual Hebrew / Greek / Aramaic processing
- [ ] Add benchmark examples and documented evaluation results

### Long term

- [ ] Package reusable SHAMIR components as an installable library
- [ ] Support contributor-provided analysis modules
- [ ] Build a transparent research workflow with auditable sources and evaluations

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Areas where help is especially useful include retrieval, embeddings, evaluation, tests, documentation, local-model support, and source attribution.

## Research and accuracy disclaimer

SHAMIR is experimental software. Outputs related to history, linguistics, theology, gematria, archaeology, or textual interpretation should not be treated as authoritative without independent verification and primary/academic sources.

## License

SHAMIR is released under the [MIT License](LICENSE).

## Maintainer

**Alex Ernest Slama**

Independent builder exploring open-source AI, local models, RAG, automation, and reproducible AI-assisted research workflows.
