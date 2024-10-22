#!/bin/bash

# Ensure that the script exits on error
set -e

cd ../
echo "Root repository path: $(pwd)"
(crontab -l 2>/dev/null; echo "*/30 * * * * $(pwd)/.venv/bin/python3 $(pwd)/scraper.py") | crontab -

# Confirm set crontab task
echo "✅ Set scheduled task collect data every 30 minut"
crontab -l
