import app as app_module


class FakePipeline:
    def analyze(self, query):
        return {
            "query": query,
            "mode": {"rag_enabled": False, "generation_enabled": False},
            "sources": [],
            "analysis_layers": [],
            "synthesis": {"status": "not_generated", "content": "test"},
            "warnings": [],
        }

    def health(self):
        return {
            "rag_enabled": False,
            "generation_enabled": False,
            "indexed_documents": None,
            "llm_model": None,
            "warnings": [],
        }


def test_health_endpoint(monkeypatch):
    monkeypatch.setattr(app_module, "pipeline", FakePipeline())
    client = app_module.app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["service"] == "SHAMIR"
    assert payload["pipeline"]["rag_enabled"] is False


def test_analyze_requires_query(monkeypatch):
    monkeypatch.setattr(app_module, "pipeline", FakePipeline())
    client = app_module.app.test_client()

    response = client.post("/api/analyze", json={})

    assert response.status_code == 400
    assert response.get_json()["status"] == "error"


def test_analyze_returns_pipeline_result(monkeypatch):
    monkeypatch.setattr(app_module, "pipeline", FakePipeline())
    client = app_module.app.test_client()

    response = client.post("/api/analyze", json={"query": "test question"})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "success"
    assert payload["query"] == "test question"
