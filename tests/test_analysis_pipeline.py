from pathlib import Path

from scripts.analysis_pipeline import BiblicalAnalysisPipeline


class FakeRetriever:
    def count(self):
        return 1

    def retrieve(self, query, n_results=5):
        assert query == "What is the context?"
        return [
            {
                "id": "source-1",
                "text": "A local source passage used for testing.",
                "metadata": {"book": "Example"},
                "distance": 0.05,
            }
        ]


class FakeGenerator:
    model = "fake-local-model"

    def generate(self, system_prompt, user_prompt):
        assert "[S1]" in user_prompt
        assert "local source" in user_prompt.lower()
        return "Grounded test response [S1]"


def test_pipeline_propagates_sources_and_generation(tmp_path: Path):
    pipeline = BiblicalAnalysisPipeline(
        retriever=FakeRetriever(),
        generator=FakeGenerator(),
        results_dir=tmp_path,
    )

    result = pipeline.analyze("What is the context?")

    assert result["mode"] == {"rag_enabled": True, "generation_enabled": True}
    assert result["sources"][0]["label"] == "S1"
    assert result["sources"][0]["id"] == "source-1"
    assert len(result["analysis_layers"]) == 4
    assert all(layer["status"] == "generated" for layer in result["analysis_layers"])
    assert result["synthesis"]["status"] == "generated"
    assert (tmp_path / "analysis_results.json").exists()


def test_pipeline_is_transparent_when_generation_is_disabled(tmp_path: Path):
    pipeline = BiblicalAnalysisPipeline(
        retriever=FakeRetriever(),
        generator=None,
        results_dir=tmp_path,
    )
    # Explicitly disable the automatically configured generator for this unit test.
    pipeline.generator = None

    result = pipeline.analyze("What is the context?")

    assert result["mode"]["rag_enabled"] is True
    assert result["mode"]["generation_enabled"] is False
    assert all(layer["status"] == "not_generated" for layer in result["analysis_layers"])
    assert result["synthesis"]["status"] == "not_generated"


def test_pipeline_rejects_empty_query(tmp_path: Path):
    pipeline = BiblicalAnalysisPipeline(retriever=None, generator=None, results_dir=tmp_path)
    pipeline.retriever = None
    pipeline.generator = None

    try:
        pipeline.analyze("   ")
    except ValueError as exc:
        assert "Query is required" in str(exc)
    else:
        raise AssertionError("Expected ValueError for empty query")
