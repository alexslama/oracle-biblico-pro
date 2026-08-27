#!/usr/bin/env python3
"""SHAMIR Flask web application."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # `.env` loading is convenient locally but not required for the core app.
    pass

sys.path.insert(0, str(Path(__file__).parent / "scripts"))
from analysis_pipeline import BiblicalAnalysisPipeline  # noqa: E402


app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
pipeline = BiblicalAnalysisPipeline()

MAX_QUERY_LENGTH = int(os.getenv("SHAMIR_MAX_QUERY_LENGTH", "4000"))


@app.route("/")
def index():
    """Serve the main web interface."""
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Analyze a research question with the configured SHAMIR pipeline."""
    data = request.get_json(silent=True) or {}
    query = str(data.get("query", "")).strip()

    if not query:
        return jsonify({"status": "error", "message": "Query is required"}), 400
    if len(query) > MAX_QUERY_LENGTH:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Query exceeds the {MAX_QUERY_LENGTH}-character limit",
                }
            ),
            400,
        )

    try:
        result = pipeline.analyze(query)
    except ValueError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400
    except Exception:
        app.logger.exception("SHAMIR analysis failed")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Analysis failed. Check server logs and local model configuration.",
                }
            ),
            500,
        )

    return jsonify({"status": "success", **result}), 200


@app.route("/api/results")
def get_results():
    """Retrieve the most recently persisted analysis result."""
    results_file = Path("outputs/analysis_results.json")
    if not results_file.exists():
        return jsonify({"status": "error", "message": "No results found"}), 404

    try:
        with results_file.open("r", encoding="utf-8") as handle:
            results = json.load(handle)
        return jsonify({"status": "success", "results": results}), 200
    except (OSError, json.JSONDecodeError):
        app.logger.exception("Failed to read persisted SHAMIR results")
        return jsonify({"status": "error", "message": "Stored results could not be read"}), 500


@app.route("/api/health")
def health():
    """Report service and optional local-AI component status."""
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "SHAMIR",
                "version": "1.1.0",
                "pipeline": pipeline.health(),
            }
        ),
        200,
    )


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0").strip().lower() in {"1", "true", "yes", "on"}
    host = os.getenv("SHAMIR_HOST", "127.0.0.1")
    port = int(os.getenv("SHAMIR_PORT", "5000"))
    app.run(debug=debug, host=host, port=port)
