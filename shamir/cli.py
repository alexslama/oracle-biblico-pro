"""Command-line interface for SHAMIR."""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any, Dict

from scripts.analysis_pipeline import BiblicalAnalysisPipeline
from scripts.rag_store import ChromaRAGStore, load_jsonl_documents
from shamir.evaluation import evaluate_result


def _print_json(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def command_doctor(_: argparse.Namespace) -> int:
    checks: Dict[str, Any] = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "rag_requested": os.getenv("SHAMIR_ENABLE_RAG", "0"),
        "llm_requested": os.getenv("SHAMIR_ENABLE_LLM", "0"),
        "ollama_python": False,
        "chromadb_python": False,
        "ollama_service": False,
    }
    try:
        import ollama

        checks["ollama_python"] = True
        try:
            ollama.list()
            checks["ollama_service"] = True
        except Exception as exc:
            checks["ollama_service_error"] = str(exc)
    except Exception as exc:
        checks["ollama_error"] = str(exc)

    try:
        import chromadb  # noqa: F401

        checks["chromadb_python"] = True
    except Exception as exc:
        checks["chromadb_error"] = str(exc)

    checks["ready_for_base_mode"] = True
    checks["ready_for_rag_dependencies"] = bool(
        checks["ollama_python"] and checks["chromadb_python"]
    )
    checks["ready_for_local_rag"] = bool(
        checks["ready_for_rag_dependencies"] and checks["ollama_service"]
    )
    _print_json(checks)
    return 0


def command_analyze(args: argparse.Namespace) -> int:
    pipeline = BiblicalAnalysisPipeline(results_dir=args.results_dir)
    result = pipeline.analyze(args.query)
    _print_json(result)
    return 0


def command_build_rag(args: argparse.Namespace) -> int:
    documents = load_jsonl_documents(args.input)
    store = ChromaRAGStore(
        persist_dir=args.persist_dir,
        collection_name=args.collection,
        embedding_model=args.embedding_model,
    )
    indexed = store.index_documents(documents)
    _print_json(
        {
            "indexed": indexed,
            "collection": args.collection,
            "persist_dir": str(Path(args.persist_dir)),
            "embedding_model": args.embedding_model,
            "total_documents": store.count(),
        }
    )
    return 0


def command_evaluate(args: argparse.Namespace) -> int:
    result_path = Path(args.input)
    if not result_path.exists():
        _print_json({"error": f"Result file not found: {result_path}"})
        return 2

    try:
        result = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _print_json({"error": f"Could not read result JSON: {exc}"})
        return 2

    report = evaluate_result(result)
    _print_json(report)
    return 0 if report["passed"] else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shamir",
        description="Local-first source-aware research toolkit.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Inspect local SHAMIR prerequisites.")
    doctor.set_defaults(func=command_doctor)

    analyze = subparsers.add_parser("analyze", help="Run one research analysis.")
    analyze.add_argument("query", help="Research question.")
    analyze.add_argument("--results-dir", default="outputs")
    analyze.set_defaults(func=command_analyze)

    build_rag = subparsers.add_parser("build-rag", help="Index a JSONL corpus into ChromaDB.")
    build_rag.add_argument("--input", default="data/demo_corpus.jsonl")
    build_rag.add_argument("--persist-dir", default="data/vector_db")
    build_rag.add_argument("--collection", default="shamir_sources")
    build_rag.add_argument("--embedding-model", default="nomic-embed-text")
    build_rag.set_defaults(func=command_build_rag)

    evaluate = subparsers.add_parser(
        "evaluate",
        help="Audit citation-label integrity in a saved SHAMIR result.",
    )
    evaluate.add_argument("--input", default="outputs/analysis_results.json")
    evaluate.set_defaults(func=command_evaluate)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
