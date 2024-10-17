#!/bin/bash

# Ensure that the script exits on error
set -e

cd ../
echo "Root repository path: $(pwd)"

.venv/bin/streamlit run app.py
