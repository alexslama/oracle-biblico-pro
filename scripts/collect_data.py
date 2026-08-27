#!/usr/bin/env python3
"""Create a small demo metadata manifest for SHAMIR development.

This script does not download Bible texts or scholarly resources. It only
creates a tiny local metadata fixture that can be used while developing data
pipelines. Real corpora must be supplied separately with appropriate rights.
"""

from __future__ import annotations

import json
from pathlib import Path


def create_demo_metadata(output_path: str | Path = "data/raw/bible_metadata.json") -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    demo_data = {
        "status": "demo_metadata_only",
        "warning": "No biblical text is included in this file.",
        "books": [
            {
                "name": "Genesis",
                "chapters": 50,
                "languages": ["Hebrew", "translation-dependent"],
            },
            {
                "name": "Exodus",
                "chapters": 40,
                "languages": ["Hebrew", "translation-dependent"],
            },
        ],
    }

    with output.open("w", encoding="utf-8") as handle:
        json.dump(demo_data, handle, ensure_ascii=False, indent=2)

    return output


def main() -> None:
    output = create_demo_metadata()
    print(f"Demo metadata written to {output}")
    print("No corpus or external reference text was downloaded.")


if __name__ == "__main__":
    main()
