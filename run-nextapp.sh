#!/bin/bash
# run-nextapp.sh - Wrapper script for Next.js pkg application

# Print banner
echo "======================================================"
echo "Next.js Application Launcher"
echo "======================================================"

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PATH="$SCRIPT_DIR/mmp"

# Check if the packaged app exists
if [ ! -f "$APP_PATH" ]; then
echo "❌ Error: Could not find the application at $APP_PATH"
echo "   Please run this script from the same directory as the 'next-app' executable."
exit 1
fi

# Find Python executable - PRIORITIZE CONDA ENVIRONMENT
CONDA_PYTHON="$HOME/miniconda3/envs/finetune/bin/python"
PYTHON_PATH=""

# Check conda environment first
if [ -f "$CONDA_PYTHON" ]; then
    PYTHON_PATH="$CONDA_PYTHON"
    echo "✅ Using conda environment Python"
# Fallback to system Python
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_PATH=$(which python3)
    echo "⚠️  Using system Python3 (conda environment not found)"
elif command -v python >/dev/null 2>&1; then
    PYTHON_PATH=$(which python)
    echo "⚠️  Using system Python (conda environment not found)"
else
    echo "❌ Error: Python not found. Please install Python 3 and try again."
    echo "   You can download Python from: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_PATH --version 2>&1)
echo "✅ Found $PYTHON_VERSION at $PYTHON_PATH"

# Export Python path for the application to use
export PYTHON_EXECUTABLE="$PYTHON_PATH"

echo "🚀 Starting Next.js application..."
echo "   Application: $APP_PATH"
echo "   Python: $PYTHON_PATH"
echo ""

# Start the application and pass through all arguments
exec "$APP_PATH" "$@"
