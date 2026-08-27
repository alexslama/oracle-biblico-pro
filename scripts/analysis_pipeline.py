#!/usr/bin/env python3
"""Grounded multi-layer analysis pipeline for SHAMIR.

The pipeline can run in three useful modes:
- base mode: no external services required; returns transparent placeholders;
- RAG mode: retrieves local sources from ChromaDB;
- RAG + LLM mode: retrieves sources and asks a local Ollama model to analyze them.

External services are opt-in through environment variables so the web app can
start safely on machines that have not configured Ollama or ChromaDB yet.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from .rag_store import ChromaRAGStore
except ImportError:  # Support direct execution from scripts/.
    from rag_store import ChromaRAGStore


TRUTHY = {"1", "true", "yes", "on"}


def _enabled(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in TRUTHY


class OllamaGenerator:
    """Thin wrapper around a locally running Ollama chat model."""

    def __init__(self, model: str = "llama3.1") -> None:
        self.model = model

    @staticmethod
    def _message_content(response: Any) -> str:
        if isinstance(response, dict):
            message = response.get("message") or {}
            if isinstance(message, dict):
                return str(message.get("content") or "").strip()
        message = getattr(response, "message", None)
        if message is not None:
            return str(getattr(message, "content", "") or "").strip()
        return ""

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        import ollama  # Lazy import: optional unless local generation is enabled.

        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            options={"temperature": 0.2},
        )
        content = self._message_content(response)
        if not content:
            raise RuntimeError("Ollama returned an empty response")
        return content


class BiblicalAnalysisPipeline:
    """Source-aware five-layer biblical research pipeline."""

    LAYERS = [
        (
            "linguistic",
            "Analyze language, semantics, grammar, translation ambiguity, and original-language considerations. "
            "Do not claim Hebrew/Greek/Aramaic facts unless they are supported by the supplied context or clearly marked as uncertain.",
        ),
        (
            "numerical",
            "Analyze numerical patterns or gematria only when the evidence supports doing so. Distinguish observed data from interpretive tradition.",
        ),
        (
            "historical",
            "Analyze historical, archaeological, cultural, and chronological context. Separate evidence from speculation.",
        ),
        (
            "theological",
            "Analyze theological themes and interpretive traditions while acknowledging that traditions may disagree.",
        ),
    ]

    def __init__(
        self,
        retriever: Optional[Any] = None,
        generator: Optional[Any] = None,
        results_dir: str | Path = "outputs",
    ) -> None:
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.warnings: List[str] = []

        self.retriever = retriever if retriever is not None else self._default_retriever()
        self.generator = generator if generator is not None else self._default_generator()

    def _default_retriever(self) -> Optional[Any]:
        if not _enabled("SHAMIR_ENABLE_RAG"):
            return None
        try:
            return ChromaRAGStore(
                persist_dir=os.getenv("SHAMIR_VECTOR_DB", "data/vector_db"),
                collection_name=os.getenv("SHAMIR_COLLECTION", "shamir_sources"),
                embedding_model=os.getenv("SHAMIR_EMBEDDING_MODEL", "nomic-embed-text"),
            )
        except Exception as exc:
            self.warnings.append(f"RAG disabled at startup: {exc}")
            return None

    def _default_generator(self) -> Optional[Any]:
        if not _enabled("SHAMIR_ENABLE_LLM"):
            return None
        try:
            return OllamaGenerator(os.getenv("SHAMIR_LLM_MODEL", "llama3.1"))
        except Exception as exc:
            self.warnings.append(f"LLM generation disabled at startup: {exc}")
            return None

    @staticmethod
    def _source_payload(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        payload: List[Dict[str, Any]] = []
        for index, source in enumerate(sources, start=1):
            payload.append(
                {
                    "label": f"S{index}",
                    "id": source.get("id"),
                    "text": source.get("text", ""),
                    "metadata": source.get("metadata") or {},
                    "distance": source.get("distance"),
                }
            )
        return payload

    @staticmethod
    def _format_context(sources: List[Dict[str, Any]]) -> str:
        if not sources:
            return "No local sources were retrieved."

        blocks: List[str] = []
        for source in sources:
            metadata = json.dumps(source.get("metadata") or {}, ensure_ascii=False, sort_keys=True)
            blocks.append(
                f"[{source['label']}]\n"
                f"Metadata: {metadata}\n"
                f"Text: {source.get('text', '')}"
            )
        return "\n\n".join(blocks)

    def _retrieve(self, query: str) -> List[Dict[str, Any]]:
        if self.retriever is None:
            return []
        try:
            n_results = int(os.getenv("SHAMIR_TOP_K", "5"))
            raw_sources = self.retriever.retrieve(query, n_results=max(1, n_results))
            return self._source_payload(raw_sources)
        except Exception as exc:
            self.warnings.append(f"Retrieval failed for this request: {exc}")
            return []

    def _generate_layer(
        self,
        layer_name: str,
        instructions: str,
        query: str,
        context: str,
    ) -> Dict[str, Any]:
        if self.generator is None:
            return {
                "name": layer_name,
                "status": "not_generated",
                "content": (
                    "Local LLM generation is disabled. Enable SHAMIR_ENABLE_LLM=1 "
                    "to generate this layer from retrieved evidence."
                ),
            }

        system_prompt = (
            "You are SHAMIR, an evidence-conscious research assistant for biblical-text study. "
            "Use only the supplied local source context for factual claims. Cite supporting source labels like [S1]. "
            "If evidence is missing, say so explicitly. Never invent quotations, manuscript facts, archaeology, dates, or citations. "
            "Treat theology and gematria as interpretive domains and distinguish interpretation from verifiable evidence."
        )
        user_prompt = (
            f"Research question: {query}\n\n"
            f"Analysis layer: {layer_name}\n"
            f"Layer instructions: {instructions}\n\n"
            f"Retrieved context:\n{context}\n\n"
            "Return a concise analysis with explicit uncertainty where appropriate."
        )
        content = self.generator.generate(system_prompt, user_prompt)
        return {"name": layer_name, "status": "generated", "content": content}

    def _generate_synthesis(self, query: str, context: str, layers: List[Dict[str, Any]]) -> Dict[str, Any]:
        if self.generator is None:
            return {
                "status": "not_generated",
                "content": "Integrated synthesis requires local LLM generation to be enabled.",
            }

        layer_text = "\n\n".join(
            f"{layer['name']}: {layer.get('content', '')}" for layer in layers
        )
        system_prompt = (
            "Synthesize research conservatively. Preserve disagreements and uncertainty, cite retrieved source labels [S#], "
            "and do not introduce facts not present in the supplied context or layer analyses."
        )
        user_prompt = (
            f"Research question: {query}\n\n"
            f"Retrieved context:\n{context}\n\n"
            f"Layer analyses:\n{layer_text}\n\n"
            "Produce an integrated synthesis and a short 'verification needed' section."
        )
        return {"status": "generated", "content": self.generator.generate(system_prompt, user_prompt)}

    def analyze(self, query: str) -> Dict[str, Any]:
        query = str(query or "").strip()
        if not query:
            raise ValueError("Query is required")

        self.warnings = [warning for warning in self.warnings if "startup" in warning.lower()]
        sources = self._retrieve(query)
        context = self._format_context(sources)

        layers = [
            self._generate_layer(name, instructions, query, context)
            for name, instructions in self.LAYERS
        ]
        synthesis = self._generate_synthesis(query, context, layers)

        result = {
            "query": query,
            "mode": {
                "rag_enabled": self.retriever is not None,
                "generation_enabled": self.generator is not None,
            },
            "sources": sources,
            "analysis_layers": layers,
            "synthesis": synthesis,
            "warnings": list(self.warnings),
        }

        output_file = self.results_dir / "analysis_results.json"
        with output_file.open("w", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)

        return result

    def health(self) -> Dict[str, Any]:
        rag_count: Optional[int] = None
        if self.retriever is not None and hasattr(self.retriever, "count"):
            try:
                rag_count = int(self.retriever.count())
            except Exception:
                rag_count = None

        return {
            "rag_enabled": self.retriever is not None,
            "generation_enabled": self.generator is not None,
            "indexed_documents": rag_count,
            "llm_model": getattr(self.generator, "model", None),
            "warnings": list(self.warnings),
        }


def main() -> None:
    pipeline = BiblicalAnalysisPipeline()
    result = pipeline.analyze("Example research question")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
