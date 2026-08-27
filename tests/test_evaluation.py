from shamir.evaluation import evaluate_result


def test_evaluator_accepts_valid_labels():
    result = {
        "sources": [{"label": "S1"}, {"label": "S2"}],
        "analysis_layers": [
            {"name": "historical", "status": "generated", "content": "Claim [S1]."}
        ],
        "synthesis": {"status": "generated", "content": "Synthesis [S1] [S2]."},
    }
    evaluation = evaluate_result(result)
    assert evaluation["passed"] is True
    assert evaluation["citation_validity"] == 1.0
    assert evaluation["source_coverage"] == 1.0


def test_evaluator_flags_invalid_and_missing_citations():
    result = {
        "sources": [{"label": "S1"}],
        "analysis_layers": [
            {"name": "linguistic", "status": "generated", "content": "Unsupported label [S9]."},
            {"name": "historical", "status": "generated", "content": "No citation here."},
        ],
        "synthesis": {"status": "not_generated", "content": ""},
    }
    evaluation = evaluate_result(result)
    assert evaluation["passed"] is False
    assert evaluation["invalid_citations"] == ["S9"]
    assert evaluation["generated_sections_without_citations"] == ["historical"]
