#!/usr/bin/env python3
"""Run a fixed SHAMIR question set and summarize citation-integrity results.

This benchmark is meaningful only when SHAMIR is configured for the intended
RAG/LLM environment. It records failures rather than hiding them.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from scripts.analysis_pipeline import BiblicalAnalysisPipeline
from shamir.evaluation import evaluate_result


def load_questions(path: Path) -> List[Dict[str, Any]]:
    questions: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                record = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
            if not str(record.get("question") or "").strip():
                raise ValueError(f"Missing question on line {line_number}")
            questions.append(record)
    return questions


def run_benchmark(question_path: Path, output_path: Path) -> Dict[str, Any]:
    questions = load_questions(question_path)
    run_dir = output_path.parent / "benchmark-results"
    pipeline = BiblicalAnalysisPipeline(results_dir=run_dir)

    items: List[Dict[str, Any]] = []
    generated_count = 0
    passed_count = 0

    for item in questions:
        result = pipeline.analyze(str(item["question"]))
        evaluation = evaluate_result(result)
        if result.get("mode", {}).get("generation_enabled"):
            generated_count += 1
        if evaluation.get("passed"):
            passed_count += 1
        items.append(
            {
                "id": item.get("id"),
                "question": item["question"],
                "topics": item.get("topics") or [],
                "mode": result.get("mode"),
                "source_labels": [source.get("label") for source in result.get("sources") or []],
                "warnings": result.get("warnings") or [],
                "evaluation": evaluation,
            }
        )

    report = {
        "benchmark_scope": "demo_question_set_and_citation_label_integrity",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "question_file": str(question_path),
        "question_count": len(questions),
        "generation_enabled_runs": generated_count,
        "deterministic_checks_passed": passed_count,
        "items": items,
        "limitations": [
            "This benchmark does not establish factual or scholarly correctness.",
            "Citation-label integrity does not prove semantic claim support.",
            "The included demo corpus is not a scholarly corpus.",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the SHAMIR demo benchmark.")
    parser.add_argument("--questions", default="benchmarks/questions.jsonl")
    parser.add_argument("--output", default="outputs/benchmark_report.json")
    args = parser.parse_args()

    report = run_benchmark(Path(args.questions), Path(args.output))
    print(json.dumps({
        "question_count": report["question_count"],
        "generation_enabled_runs": report["generation_enabled_runs"],
        "deterministic_checks_passed": report["deterministic_checks_passed"],
        "output": args.output,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
