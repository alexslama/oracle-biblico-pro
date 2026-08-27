# SHAMIR Web Interface and API Guide

This document describes the current Flask interface exposed by SHAMIR. For installation, RAG setup, local Ollama configuration, and project status, see [README.md](README.md) and [QUICK_START.md](QUICK_START.md).

## Start the server

```bash
source venv/bin/activate
python3 app.py
```

Default address:

```text
http://127.0.0.1:5000
```

You can change the bind address and port with:

```bash
export SHAMIR_HOST=127.0.0.1
export SHAMIR_PORT=8000
python3 app.py
```

`FLASK_DEBUG` is off by default.

## API endpoints

### `GET /api/health`

Reports the service version and the state of optional local components.

Example:

```json
{
  "status": "healthy",
  "service": "SHAMIR",
  "version": "1.1.0",
  "pipeline": {
    "rag_enabled": false,
    "generation_enabled": false,
    "indexed_documents": null,
    "llm_model": null,
    "warnings": []
  }
}
```

### `POST /api/analyze`

Request:

```json
{
  "query": "What evidence supports this interpretation?"
}
```

Successful responses include:

- `mode` — whether local RAG and LLM generation are enabled;
- `sources` — retrieved local documents and metadata;
- `analysis_layers` — linguistic, numerical, historical, and theological outputs;
- `synthesis` — integrated output when local generation is available;
- `warnings` — retrieval or generation problems that should remain visible.

Base mode is deliberately transparent: when generation is disabled, analysis layers return `not_generated` rather than synthetic scholarly claims.

### `GET /api/results`

Returns the most recent JSON result persisted to:

```text
outputs/analysis_results.json
```

## cURL examples

Health:

```bash
curl http://127.0.0.1:5000/api/health
```

Analyze:

```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"query":"What evidence supports this interpretation?"}'
```

## JavaScript example

```javascript
const response = await fetch('/api/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({query: 'What evidence supports this interpretation?'})
});

const data = await response.json();
console.log(data);
```

## Local RAG / LLM status

To enable the bundled RAG demo:

```bash
ollama pull nomic-embed-text
python3 scripts/build_rag.py
export SHAMIR_ENABLE_RAG=1
python3 app.py
```

To add local generation:

```bash
ollama pull llama3.1
export SHAMIR_ENABLE_RAG=1
export SHAMIR_ENABLE_LLM=1
export SHAMIR_LLM_MODEL=llama3.1
python3 app.py
```

Always confirm the current pipeline state with `/api/health`.

## Input and error behavior

- empty queries return HTTP `400`;
- queries longer than `SHAMIR_MAX_QUERY_LENGTH` return HTTP `400`;
- internal server exceptions are logged but are not returned verbatim to the client;
- Ollama generation failures are represented as `generation_failed` plus a warning instead of crashing the full request when possible.

## UI notes

The repository includes the existing HTML/CSS/JavaScript interface under `templates/` and `static/`. The UI is currently a lightweight research front-end over the Flask API, not a claim of production readiness.

## Security notes

- do not expose the development Flask server directly to the public internet;
- do not index secrets, credentials, or private data unless you understand the storage implications;
- treat local model output as untrusted content;
- review [SECURITY.md](SECURITY.md) before building a public service on top of SHAMIR.

## Current limitations

SHAMIR does not currently provide authentication, rate limiting, multi-user isolation, formal academic citation management, or production deployment configuration. Those should be added before any public multi-user deployment.
