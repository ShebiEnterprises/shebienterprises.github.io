#!/usr/bin/env sh
# Local static server with live reload on file changes.
# Usage: ./serve.sh
#   PORT=3000 ./serve.sh   - custom port (default 8080)
#   NO_OPEN=1 ./serve.sh   - do not open a browser tab
#
# Requires: Node.js (for npx). First run may download live-server from npm.

set -e
cd "$(dirname "$0")"

PORT="${PORT:-8080}"
HOST="${HOST:-127.0.0.1}"

if [ -z "${NO_OPEN:-}" ]; then
  exec npx --yes live-server --port="$PORT" --host="$HOST" --open=/index.html .
else
  exec npx --yes live-server --port="$PORT" --host="$HOST" .
fi
