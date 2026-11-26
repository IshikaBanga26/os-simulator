#!/usr/bin/env bash
# Launch the simulator after checking Python is available.
set -e
cd "$(dirname "$0")/.."

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required but not installed." >&2
  exit 1
fi

mkdir -p outputs/logs
echo "Using $(python3 --version)"
python3 main.py
