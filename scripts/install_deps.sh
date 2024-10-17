#!/bin/bash

# Ensure that the script exits on error
set -e

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python could not be found. Please install Python and try again."
    exit 1
fi

# Install packages from a requirements file (optional)
cd ../
echo "Root repository path: $(pwd)"
python3 -m venv .venv

.venv/bin/python3 -m pip install --upgrade pip
.venv/bin/python3 -m pip install -r requirements.txt

# Confirm installation
echo "✅ Python packages installed successfully."
