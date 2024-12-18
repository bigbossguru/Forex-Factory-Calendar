#!/bin/bash

# Ensure that the script exits on error
set -e

cd ../
echo "Root repository path: $(pwd)"

# Confirm unset crontab task
(crontab -l | grep -v "\*/5 \* \* \* \* $(pwd)/.venv/bin/python3 $(pwd)/scraper.py") | crontab -
(crontab -l | grep -v "\*/30 \* \* \* \* $(pwd)/.venv/bin/python3 $(pwd)/scraper.py") | crontab -
(crontab -l | grep -v "\*/10 \* \* \* \* $(pwd)/.venv/bin/python3 $(pwd)/scraper.py") | crontab -


# Confirm set crontab task
echo "✅ Unset schedule task"
crontab -l
