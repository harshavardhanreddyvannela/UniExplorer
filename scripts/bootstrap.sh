#!/usr/bin/env zsh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required. Install latest stable Python and rerun."
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required. Install latest stable Node.js and rerun."
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

cd frontend
npm install

echo "Bootstrap complete."
echo "Backend: source .venv/bin/activate && uvicorn backend.app.main:app --reload"
echo "Frontend: cd frontend && npm run dev"
echo "Lint: ruff check . && cd frontend && npm run lint"
