#!/usr/bin/env bash
# Runs all tests and saves a timestamped report in outputs/logs/.
cd "$(dirname "$0")/.." || exit 1
mkdir -p outputs/logs
out="outputs/logs/test_run_$(date +%Y%m%d_%H%M%S).txt"
python3 -m unittest discover -s tests -t . -v 2>&1 | tee "$out"
echo "Report saved to $out"
