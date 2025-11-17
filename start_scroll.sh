#!/bin/bash

# 1. Determine the full path of the running script ($0).
# We use readlink -f to resolve any symlinks and get the absolute path.
SCRIPT_PATH=$(readlink -f "$0")

# 2. Extract the project directory (the path where this start_scroll.sh script is located)
PROJECT_DIR=$(dirname "$SCRIPT_PATH")

# Make sure to update the Python script name to your latest version if necessary.
SCRIPT_NAME="enhanced_scroll.py" # Assuming the final name for the Python script

# Change the working directory to the project directory
cd "$PROJECT_DIR" || { echo "Error: Could not change directory to $PROJECT_DIR"; exit 1; }

# 3. Activate the Python virtual environment
# Ensure that "venv" is the correct name for your virtual environment.
source venv/bin/activate

# 4. Run the Python script
# "&" runs the script in the background.
python "$SCRIPT_NAME" &

# 'disown' allows the script to continue running even if the parent process closes.
disown

echo "Scroll accelerator script has been started."
