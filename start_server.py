#!/usr/bin/env python3
"""
MoonHub Inventory Management System - Development Server
Production-ready startup script with enhanced features
"""

import os
import sys
import time
import threading
import webbrowser
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from web_dashboard import app
    from inventory_manager import InventoryManager
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("📝 Please run: pip install -r requirements.txt")
    sys.exit(1)

def setup_directories():
    """Create necessary directories"""
    directories = ['logs', 'configs', 'backups', 'exports', 'uploads']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def initialize_database():
    """Initialize database with sample data if needed"""
    try:
        inventory = InventoryManager()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
        return False

def open_browser():
    """Open browser after server starts"""
    time.sleep(3)
    try:
        webbrowser.open('http://localhost:8080')
        print("🌐 Browser opened automatically")
    except Exception as e:
        print(f"⚠️ Could not open browser: {e}")
        print("🌐 Please open http://localhost:8080 manually")

def print_startup_info():
    """Print startup information"""
    print("🌙" + "=" * 60)
    print("🌙 MoonHub Inventory Management System - 2025")
    print("🌙 Production-Ready E-commerce Solution")
    print("🌙" + "=" * 60)
    print(f"🚀 Starting development server...")
    print(f"🌐 Dashboard URL: http://localhost:8080")
    print(f"🔐 Default Login: admin / admin123")
    print(f"📈 Features: Multi-platform, Real-time Analytics, Automation")
    print("🌙" + "=" * 60)

def check_dependencies():
    """Check if required dependencies are installed"""
    required_modules = [
        'flask', 'pandas', 'numpy', 'openpyxl', 
        'plotly', 'requests', 'werkzeug'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing dependencies: {', '.join(missing_modules)}")
        print("📝 Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def main():
    """Main startup function"""
    print_startup_info()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    print("✅ Directory structure created")
    
    # Initialize database
    initialize_database()
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_APP'] = 'web_dashboard.py'
    
    # Start browser in separate thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        print("✅ Server starting on http://localhost:8080")
        print("📝 Press Ctrl+C to stop the server")
        print("🌙" + "-" * 60)
        
        # Start Flask development server
        app.run(
            debug=False,
            host='0.0.0.0',
            port=8080,
            use_reloader=False,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        print("📝 Check logs for more details")
    finally:
        print("🌙 Thank you for using MoonHub 2025!")

if __name__ == '__main__':
    main()