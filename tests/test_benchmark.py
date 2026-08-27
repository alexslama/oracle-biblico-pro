import json

import pytest

from scripts.run_benchmark import load_questions


def test_load_questions(tmp_path):
    path = tmp_path / "questions.jsonl"
    path.write_text(
        json.dumps({"id": "q1", "question": "What is tested?"}) + "\n",
        encoding="utf-8",
    )
    questions = load_questions(path)
    assert questions == [{"id": "q1", "question": "What is tested?"}]


def test_load_questions_requires_question(tmp_path):
    path = tmp_path / "questions.jsonl"
    path.write_text(json.dumps({"id": "q1"}) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Missing question"):
        load_questions(path)
