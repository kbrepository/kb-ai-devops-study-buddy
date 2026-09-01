#!/bin/bash

set -e

echo "Running KB AI DevOps Study Buddy preflight checks..."

python preflight_check.py

echo ""
echo "Starting Streamlit..."

python -m streamlit run streamlit_app.py