#!/bin/bash
cd /app
echo "=== Files in /app ==="
ls -la
echo "=== Python files ==="
find /app -name "*.py" -type f

echo "=== Running taunt bot ==="
python /app/hazbin_timeout_taunt_bot.py
