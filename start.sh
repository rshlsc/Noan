#!/bin/bash
# Script to start the Noan application on Render

# Print the Python version (for debugging)
echo "Python version:"
python --version

# Print the installed packages (for debugging)
echo "Installed packages:"
pip list

# Check if gunicorn is installed
if ! command -v gunicorn &> /dev/null; then
    echo "gunicorn not found, installing..."
    pip install gunicorn
fi

# Start the application
echo "Starting Noan..."
exec python -m gunicorn app:app 