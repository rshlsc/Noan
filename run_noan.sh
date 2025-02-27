#!/bin/bash
# Script to run the Noan application with virtual environment
# The application will be available at http://localhost:3000

# Activate the virtual environment
source noan_env/bin/activate

# Run the application
python3 Noan.py

# This script can be run with: bash run_noan.sh 