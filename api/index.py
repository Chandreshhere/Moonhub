import sys
import os
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)

# Set temp directory for Vercel
os.environ['TMPDIR'] = '/tmp'

from web_dashboard import app
