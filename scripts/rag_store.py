#!/usr/bin/env python3
"""Local-first retrieval primitives for SHAMIR.

This module keeps optional third-party imports lazy so the Flask application can
start even when the RAG stack is not installed or configured.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence


class OllamaEmbedder:
    """Create embeddings using a locally running Ollama server."""

    def __init__(self, model: str = "nomic-embed-text") -> None:
        self.model = model

    @staticmethod
    def _value(response: Any, key: str) -> Any:
        if isinstance(response, dict):
            return response.get(key)
        return getattr(response, key, None)

    def embed(self, texts: Sequence[str]) -> List[List[float]]:
        if not texts:
            return []

        import ollama  # Lazy import: optional unless RAG is enabled.

        # Newer Ollama Python clients support batched `embed`.
        if hasattr(ollama, "embed"):
            response = ollama.embed(model=self.model, input=list(texts))
            vectors = self._value(response, "embeddings")
            if vectors:
                return [list(vector) for vector in vectors]

        # Compatibility path for clients exposing `embeddings` per prompt.
        vectors: List[List[float]] = []
        for text in texts:
            response = ollama.embeddings(model=self.model, prompt=text)
            vector = self._value(response, "embedding")
            if not vector:
                raise RuntimeError("Ollama did not return an embedding vector")
            vectors.append(list(vector))
        return vectors


def _normalize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Convert metadata to scalar values accepted by ChromaDB."""
    normalized: Dict[str, Any] = {}
    for key, value in metadata.items():
        if value is None:
            continue
        if isinstance(value, (str, int, float, bool)):
            normalized[str(key)] = value
        else:
            normalized[str(key)] = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return normalized


def load_jsonl_documents(path: str | Path) -> List[Dict[str, Any]]:
    """Load records with `text` plus optional `metadata` from a JSONL file."""
    source_path = Path(path)
    if not source_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {source_path}")

    documents: List[Dict[str, Any]] = []
    with source_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc

            text = str(record.get("text", "")).strip()
            if not text:
                continue

            metadata = dict(record.get("metadata") or {})
            if record.get("languages"):
                metadata.setdefault("languages", record["languages"])
            metadata.setdefault("source_file", source_path.name)
            metadata.setdefault("line_number", line_number)

            documents.append({"text": text, "metadata": metadata})

    return documents


class ChromaRAGStore:
    """Persistent ChromaDB store backed by local Ollama embeddings."""

    def __init__(
        self,
        persist_dir: str | Path = "data/vector_db",
        collection_name: str = "shamir_sources",
        embedding_model: str = "nomic-embed-text",
        embedder: Optional[Any] = None,
    ) -> None:
        import chromadb  # Lazy import: optional unless RAG is enabled.

        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.collection_name = collection_name
        self.embedder = embedder or OllamaEmbedder(embedding_model)
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    @staticmethod
    def _document_id(text: str, metadata: Dict[str, Any]) -> str:
        material = text + json.dumps(metadata, ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]

    def count(self) -> int:
        return int(self.collection.count())

    def index_documents(self, documents: Iterable[Dict[str, Any]]) -> int:
        records = [doc for doc in documents if str(doc.get("text", "")).strip()]
        if not records:
            return 0

        texts = [str(doc["text"]).strip() for doc in records]
        metadatas = [_normalize_metadata(dict(doc.get("metadata") or {})) for doc in records]
        ids = [self._document_id(text, metadata) for text, metadata in zip(texts, metadatas)]
        embeddings = self.embedder.embed(texts)

        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )
        return len(records)

    def retrieve(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        query = query.strip()
        if not query or self.count() == 0:
            return []

        query_embedding = self.embedder.embed([query])[0]
        limit = max(1, min(int(n_results), self.count()))
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            include=["documents", "metadatas", "distances"],
        )

        ids = (result.get("ids") or [[]])[0]
        documents = (result.get("documents") or [[]])[0]
        metadatas = (result.get("metadatas") or [[]])[0]
        distances = (result.get("distances") or [[]])[0]

        sources: List[Dict[str, Any]] = []
        for index, source_id in enumerate(ids):
            sources.append(
                {
                    "id": source_id,
                    "text": documents[index] if index < len(documents) else "",
                    "metadata": metadatas[index] if index < len(metadatas) else {},
                    "distance": distances[index] if index < len(distances) else None,
                }
            )
        return sources
