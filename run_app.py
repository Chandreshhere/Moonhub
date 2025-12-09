#!/usr/bin/env python3
"""
MoonHub Inventory Management System - Startup Script
Run this script to start the application
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("🌙 Starting MoonHub Inventory Management System...")
    
    # Initialize database
    try:
        from database import setup_database
        setup_database()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return
    
    # Initialize inventory manager with sample data
    try:
        from inventory_manager import InventoryManager
        inventory = InventoryManager()
        
        # Check if we have any products, if not add sample data
        report = inventory.generate_inventory_report()
        if len(report) == 0:
            print("📦 Adding sample products...")
            sample_products = [
                ("WH001", "Wireless Headphones", "Electronics", 800, 1500, 45),
                ("KB002", "Mechanical Keyboard", "Electronics", 1200, 2200, 23),
                ("MS003", "Gaming Mouse", "Electronics", 600, 1100, 67),
                ("CH004", "Phone Charger", "Accessories", 150, 350, 120),
                ("CS005", "Phone Case", "Accessories", 100, 250, 8),
                ("SP006", "Bluetooth Speaker", "Electronics", 900, 1800, 0),
                ("CB007", "USB Cable", "Accessories", 50, 150, 200),
                ("TB008", "Tablet Stand", "Accessories", 300, 650, 35)
            ]
            
            for sku, name, category, cost, selling, stock in sample_products:
                inventory.add_product(sku, name, category, cost, selling, stock)
            
            print(f"✅ Added {len(sample_products)} sample products")
        else:
            print(f"✅ Found {len(report)} existing products")
            
    except Exception as e:
        print(f"❌ Inventory initialization failed: {e}")
        return
    
    # Start web application
    try:
        from web_dashboard import app
        print("\n🚀 Starting web server...")
        print("📱 Dashboard URL: http://localhost:8080")
        print("📊 API Endpoints:")
        print("   - Dashboard Stats: http://localhost:8080/api/dashboard-stats")
        print("   - Inventory Data: http://localhost:8080/api/inventory-data")
        print("   - Export Excel: http://localhost:8080/api/export-excel")
        print("\n💡 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app.run(debug=False, host='0.0.0.0', port=8080)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")

if __name__ == '__main__':
    main()