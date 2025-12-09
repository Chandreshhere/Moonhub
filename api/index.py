import sys
import os
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)

# Set working directory
os.chdir(parent_dir)

from web_dashboard import app

# Vercel serverless function handler
app = app
