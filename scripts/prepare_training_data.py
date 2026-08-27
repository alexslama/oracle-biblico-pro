#!/usr/bin/env python3
"""Convert SHAMIR demo metadata into a small JSONL development fixture.

This utility is intentionally limited: it does not create a scholarly corpus,
it does not scrape copyrighted text, and it does not produce sufficient data
for real model fine-tuning. It exists only to exercise local data pipelines.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class DemoDataPreparator:
    """Prepare metadata-only JSONL records for development tests."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.processed_dir = self.data_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def load_demo_metadata(self) -> Dict[str, Any]:
        source = self.data_dir / "raw" / "bible_metadata.json"
        if not source.exists():
            return {"books": []}
        with source.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def create_records(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        for book in data.get("books", []):
            name = str(book.get("name", "")).strip()
            chapters = book.get("chapters")
            if not name:
                continue
            records.append(
                {
                    "text": (
                        f"SHAMIR development metadata note: {name} is represented "
                        f"in this fixture with {chapters} chapters. This is metadata, not source text."
                    ),
                    "metadata": {
                        "book_name": name,
                        "chapter_count": chapters,
                        "kind": "demo-metadata",
                    },
                }
            )
        return records

    def save_records(self, records: List[Dict[str, Any]]) -> Path:
        output = self.processed_dir / "metadata_fixture.jsonl"
        with output.open("w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        return output

    def prepare(self) -> Path:
        data = self.load_demo_metadata()
        return self.save_records(self.create_records(data))


def main() -> None:
    output = DemoDataPreparator().prepare()
    print(f"Development metadata fixture written to {output}")
    print("No scholarly corpus or model-training dataset was created.")


if __name__ == "__main__":
    main()
