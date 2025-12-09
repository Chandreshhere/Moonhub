import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from web_dashboard import app

# For Vercel deployment
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
