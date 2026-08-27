import json

import pytest

from scripts.rag_store import load_jsonl_documents


def test_load_jsonl_documents_preserves_text_and_metadata(tmp_path):
    source = tmp_path / "corpus.jsonl"
    source.write_text(
        json.dumps(
            {
                "text": "Example source text",
                "metadata": {"source": "unit-test"},
                "languages": ["English"],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    documents = load_jsonl_documents(source)

    assert len(documents) == 1
    assert documents[0]["text"] == "Example source text"
    assert documents[0]["metadata"]["source"] == "unit-test"
    assert documents[0]["metadata"]["languages"] == ["English"]
    assert documents[0]["metadata"]["source_file"] == "corpus.jsonl"
    assert documents[0]["metadata"]["line_number"] == 1


def test_load_jsonl_documents_skips_blank_text(tmp_path):
    source = tmp_path / "corpus.jsonl"
    source.write_text('{"text":""}\n{"text":"usable"}\n', encoding="utf-8")

    documents = load_jsonl_documents(source)

    assert [document["text"] for document in documents] == ["usable"]


def test_load_jsonl_documents_reports_invalid_json_line(tmp_path):
    source = tmp_path / "corpus.jsonl"
    source.write_text('{"text":"ok"}\nnot-json\n', encoding="utf-8")

    with pytest.raises(ValueError, match="line 2"):
        load_jsonl_documents(source)
