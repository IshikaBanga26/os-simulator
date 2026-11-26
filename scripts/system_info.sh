#!/usr/bin/env bash
# Shows REAL system data to compare with the simulated results.
echo "=== Memory (MB) ==="
free -m
echo
echo "=== Disk usage (/) ==="
df -h /
echo
echo "=== Top 5 processes by CPU ==="
ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -6
