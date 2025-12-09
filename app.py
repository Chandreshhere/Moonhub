import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from web_dashboard import app

if __name__ == '__main__':
    app.run()
