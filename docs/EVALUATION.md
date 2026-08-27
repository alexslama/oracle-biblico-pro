# Evaluation methodology

SHAMIR separates **auditable mechanical checks** from claims about semantic truth.

## What is implemented today

`shamir.evaluation.evaluate_result()` validates citation-label integrity for generated sections.

It reports:

- the source labels retrieved for a request;
- every `[S#]` citation emitted by generated layers and synthesis;
- citations to labels that were never retrieved;
- generated sections that cite no retrieved source despite sources being available;
- citation validity ratio;
- source coverage ratio.

Run it from the CLI:

```bash
shamir evaluate --input outputs/analysis_results.json
```

The command exits with status `0` when the deterministic checks pass and `2` when they fail or the result file cannot be read.

## What these metrics do NOT prove

A valid label does not prove that the cited passage supports the sentence that references it. The current evaluator does **not** measure:

- factual correctness;
- semantic entailment between claim and source;
- scholarly quality of a source;
- completeness of retrieval;
- theological correctness;
- historical or linguistic consensus.

Those problems require separate datasets, human review, or additional model-assisted evaluation with clearly documented limitations.

## Recommended benchmark protocol

For a meaningful local RAG evaluation:

1. use a corpus with documented provenance and redistribution rights;
2. record the exact embedding model and chat model;
3. build a fresh vector store;
4. run a fixed question set;
5. persist all raw SHAMIR JSON results;
6. run deterministic citation integrity checks;
7. manually inspect retrieval relevance and claim-to-source support;
8. record failures instead of discarding them;
9. publish model/version/environment information with the benchmark.

## Future evaluation layers

Planned work includes:

- retrieval recall/precision on labeled question-source pairs;
- claim extraction followed by claim-to-source entailment scoring;
- citation completeness metrics;
- hallucination/error taxonomies;
- human-review rubrics for linguistic and historical claims;
- regression benchmarks across embedding and generation providers.

All future metrics should preserve the same rule: **state exactly what a metric measures and what it does not measure.**
