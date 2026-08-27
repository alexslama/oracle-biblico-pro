#!/usr/bin/env python3
"""Build the SHAMIR local RAG index with Ollama embeddings and ChromaDB."""

from __future__ import annotations

import argparse

try:
    from .rag_store import ChromaRAGStore, load_jsonl_documents
except ImportError:  # Support direct execution: python scripts/build_rag.py
    from rag_store import ChromaRAGStore, load_jsonl_documents


def build_index(
    input_path: str,
    persist_dir: str,
    collection: str,
    embedding_model: str,
) -> int:
    documents = load_jsonl_documents(input_path)
    if not documents:
        print(f"No indexable documents found in {input_path}")
        return 0

    store = ChromaRAGStore(
        persist_dir=persist_dir,
        collection_name=collection,
        embedding_model=embedding_model,
    )
    indexed = store.index_documents(documents)
    print(f"Indexed {indexed} documents")
    print(f"Collection: {collection}")
    print(f"Persistent store: {persist_dir}")
    print(f"Embedding model: {embedding_model}")
    print(f"Total documents in collection: {store.count()}")
    return indexed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default="data/processed/training_data.jsonl",
        help="JSONL file containing records with a text field",
    )
    parser.add_argument(
        "--persist-dir",
        default="data/vector_db",
        help="Directory used by ChromaDB for persistence",
    )
    parser.add_argument(
        "--collection",
        default="shamir_sources",
        help="ChromaDB collection name",
    )
    parser.add_argument(
        "--embedding-model",
        default="nomic-embed-text",
        help="Ollama embedding model",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_index(
        input_path=args.input,
        persist_dir=args.persist_dir,
        collection=args.collection,
        embedding_model=args.embedding_model,
    )


if __name__ == "__main__":
    main()
