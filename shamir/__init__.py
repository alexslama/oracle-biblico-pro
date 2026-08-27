"""Public Python API for SHAMIR."""

from scripts.analysis_pipeline import BiblicalAnalysisPipeline
from scripts.rag_store import ChromaRAGStore, OllamaEmbedder, load_jsonl_documents
from .evaluation import evaluate_result

__all__ = [
    "BiblicalAnalysisPipeline",
    "ChromaRAGStore",
    "OllamaEmbedder",
    "load_jsonl_documents",
    "evaluate_result",
]

__version__ = "0.2.0"
