#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "SHAMIR setup"
echo "============"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required. Install Python 3.12+ and run this script again."
  exit 1
fi

python3 - <<'PY'
import sys
if sys.version_info < (3, 12):
    raise SystemExit(f"Python 3.12+ is required; found {sys.version.split()[0]}")
print(f"Python: {sys.version.split()[0]}")
PY

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

mkdir -p data/vector_db outputs logs

echo
echo "Base installation complete."
echo "Run: source venv/bin/activate && python3 app.py"
echo

if command -v ollama >/dev/null 2>&1; then
  echo "Ollama detected. To enable the local RAG demo:"
  echo "  ollama pull nomic-embed-text"
  echo "  python3 scripts/build_rag.py"
  echo "  export SHAMIR_ENABLE_RAG=1"
  echo
  echo "For local generation:"
  echo "  ollama pull llama3.1"
  echo "  export SHAMIR_ENABLE_LLM=1"
else
  echo "Ollama was not detected. Base mode still works without it."
  echo "Install Ollama separately if you want local embeddings or generation."
fi
