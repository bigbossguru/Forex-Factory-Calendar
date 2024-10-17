#!/bin/bash

# Ensure that the script exits on error
set -e

cd ../
echo "Root repository path: $(pwd)"
(crontab -l 2>/dev/null; echo "*/5 * * * * $(pwd)/.venv/bin/python3 $(pwd)/scraper.py") | crontab -

# Confirm set crontab task
echo "✅ Set schedule task every day at 17:00 CEST"
crontab -l
