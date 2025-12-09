import sys
import os
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)

# Set temp directory for Vercel
os.environ['TMPDIR'] = '/tmp'

try:
    from web_dashboard import app
except Exception as e:
    print(f"Error importing app: {e}")
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({'error': 'App initialization failed', 'details': str(e)})

# Vercel handler
handler = app
