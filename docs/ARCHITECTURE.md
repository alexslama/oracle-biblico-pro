# SHAMIR Architecture

SHAMIR is designed as a local-first research toolkit with explicit separation between retrieval, generation, evaluation, and presentation.

## Execution modes

1. **Base mode** — no external services. The pipeline validates input, persists a transparent result, and reports that model-backed sections were not generated.
2. **RAG mode** — ChromaDB + Ollama embeddings retrieve local corpus passages and expose them as labeled sources (`S1`, `S2`, ...).
3. **RAG + LLM mode** — retrieved sources are supplied to a local Ollama chat model. Generated sections are instructed to cite only retrieved labels and to surface uncertainty.

## Main components

```text
JSONL corpus
   |
   v
Ollama embeddings ---> ChromaDB persistent collection
                           |
question ----------------> retrieval
                           |
                           v
                     labeled sources
                      S1, S2, ...
                           |
                           v
                  analysis pipeline
                 /   /   |   \   \
        linguistic ... theological
                 \   \   |   /   /
                           v
                       synthesis
                           |
                +----------+----------+
                |                     |
                v                     v
          persisted JSON        citation evaluator
                |                     |
                v                     v
          Flask API / CLI       auditable metrics
```

## Trust boundaries

SHAMIR deliberately does not equate retrieval with truth. Four independent things can fail:

- **source quality** — the corpus may contain weak, biased, outdated, or incorrectly licensed material;
- **retrieval quality** — relevant sources may not be returned;
- **generation quality** — the model may misread or overstate retrieved evidence;
- **citation quality** — a generated claim may cite an available label without actually being supported by that source.

The current deterministic evaluator checks only citation-label integrity. Semantic entailment and scholarly source quality remain separate evaluation problems.

## Failure semantics

The application avoids silently pretending that optional AI services worked:

- `not_generated` means local generation is disabled;
- `generation_failed` means a generation attempt failed;
- retrieval failures are recorded in `warnings`;
- the API returns sanitized server errors instead of exposing internal exception details.

## Data flow

A corpus record is a JSON object containing `text` and optional `metadata`. During indexing, metadata is normalized to scalar values supported by ChromaDB. Document IDs are deterministic hashes of text + normalized metadata, making repeated indexing idempotent through Chroma upserts.

At query time, retrieved documents are assigned request-local labels. These labels are the only citation identifiers supplied to the model and evaluator.

## Extension points

Future provider interfaces should preserve the same contracts:

- `embed(texts) -> vectors`
- `retrieve(query, n_results) -> sources`
- `generate(system_prompt, user_prompt) -> text`
- `evaluate_result(result) -> report`

This keeps the research pipeline independent of any single model or vector database while retaining transparent failure states and source provenance.
