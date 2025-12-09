#!/usr/bin/env python3
"""
Simple MoonHub Startup Script
"""
import os
import sys

def main():
    print("🌙 MoonHub Inventory Management System")
    print("=" * 50)
    
    try:
        from app import app, add_sample_data
        
        print("✅ Database initialized")
        add_sample_data()
        print("✅ Sample data loaded")
        print("\n🚀 Starting server...")
        print("📱 Open your browser: http://localhost:8080")
        print("💡 Press Ctrl+C to stop")
        print("-" * 50)
        
        app.run(debug=False, host='0.0.0.0', port=8080)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()