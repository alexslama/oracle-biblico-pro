# SHAMIR CLI

After installing the project in editable mode:

```bash
python -m pip install -e .
```

the `shamir` command becomes available.

## Diagnose the local environment

```bash
shamir doctor
```

Reports Python/platform information, whether Ollama and ChromaDB Python dependencies are installed, whether the local Ollama service can be reached, and whether the environment is ready for base mode or local RAG.

## Build the local vector index

```bash
shamir build-rag --input data/demo_corpus.jsonl
```

Optional flags:

```text
--persist-dir data/vector_db
--collection shamir_sources
--embedding-model nomic-embed-text
```

This requires a running Ollama service and the configured embedding model.

## Analyze a question

```bash
shamir analyze "What does the local corpus say about Torah?"
```

SHAMIR's environment variables determine whether the command runs in base, RAG, or RAG+LLM mode.

Example:

```bash
export SHAMIR_ENABLE_RAG=1
export SHAMIR_ENABLE_LLM=1
export SHAMIR_LLM_MODEL=llama3.1
shamir analyze "What does the local corpus say about Torah?"
```

## Evaluate citation-label integrity

```bash
shamir evaluate --input outputs/analysis_results.json
```

This command checks whether generated `[S#]` labels correspond to sources that were actually retrieved and whether generated sections cite retrieved sources when sources are available.

It deliberately does **not** claim to prove that a citation semantically supports a factual claim. See [EVALUATION.md](EVALUATION.md).

## Run the demo benchmark

```bash
python scripts/run_benchmark.py \
  --questions benchmarks/questions.jsonl \
  --output outputs/benchmark_report.json
```

The benchmark preserves failures and records deterministic citation-integrity reports for the fixed demo question set.
