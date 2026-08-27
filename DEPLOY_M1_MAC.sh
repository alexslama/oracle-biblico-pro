#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

ARCH="$(uname -m)"
if [ "$ARCH" = "arm64" ]; then
  echo "Apple Silicon detected (arm64)."
else
  echo "This helper was named for Apple Silicon, but the core setup is platform-neutral."
  echo "Detected architecture: $ARCH"
fi

echo "Running the reproducible SHAMIR setup..."
exec bash "$ROOT_DIR/setup.sh"
