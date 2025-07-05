#!/bin/bash
# run.sh for Linux/macOS

# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# 4. Run FastAPI app
uvicorn app:app --reload
