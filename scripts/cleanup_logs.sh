#!/usr/bin/env bash
# Deletes test reports older than 7 days and rotates a large activity log.
cd "$(dirname "$0")/../outputs/logs" || { echo "No logs folder."; exit 1; }
find . -name "test_run_*.txt" -mtime +7 -delete
if [ -f activity.log ] && [ "$(stat -c%s activity.log)" -gt 102400 ]; then
  mv activity.log "activity_$(date +%Y%m%d).log"
  echo "Rotated activity.log"
fi
echo "Cleanup done."
