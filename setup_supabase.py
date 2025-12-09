#!/usr/bin/env python3
"""
Supabase Database Setup Script
Run this to create all required tables
"""

import os

# Your Supabase connection details
# Get these from: Supabase Dashboard → Settings → Database → Connection String
SUPABASE_HOST = "db.xxxxxxxxx.supabase.co"  # Replace with your host
SUPABASE_PASSWORD = "your_password_here"     # Replace with your password
SUPABASE_USER = "postgres"
SUPABASE_DB = "postgres"
SUPABASE_PORT = "5432"

# Build connection URL
DATABASE_URL = f"postgresql://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_HOST}:{SUPABASE_PORT}/{SUPABASE_DB}"

print("🌙 MoonHub - Supabase Setup")
print("=" * 50)

try:
    import psycopg2
    print("✅ psycopg2 installed")
except ImportError:
    print("❌ Installing psycopg2...")
    os.system("pip install psycopg2-binary")
    import psycopg2

print("\n📡 Connecting to Supabase...")
try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("✅ Connected successfully!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\n📝 Please update the connection details in this script:")
    print("   - SUPABASE_HOST")
    print("   - SUPABASE_PASSWORD")
    exit(1)

print("\n🗄️ Creating tables...")

# Products table
print("  → Creating products table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        sku TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        category TEXT,
        cost_price REAL,
        selling_price REAL,
        current_stock INTEGER DEFAULT 0,
        min_stock_level INTEGER DEFAULT 10,
        max_stock_level INTEGER DEFAULT 100,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print("  ✅ Products table created")

# Platform listings table
print("  → Creating platform_listings table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS platform_listings (
        id SERIAL PRIMARY KEY,
        product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
        platform TEXT NOT NULL,
        platform_sku TEXT,
        platform_price REAL,
        stock_allocated INTEGER DEFAULT 0,
        is_active BOOLEAN DEFAULT TRUE,
        last_sync TIMESTAMP
    )
''')
print("  ✅ Platform listings table created")

# Stock movements table
print("  → Creating stock_movements table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_movements (
        id SERIAL PRIMARY KEY,
        product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
        movement_type TEXT,
        quantity INTEGER,
        platform TEXT,
        order_id TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print("  ✅ Stock movements table created")

# Orders table
print("  → Creating orders table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        order_id TEXT UNIQUE,
        platform TEXT,
        product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
        quantity INTEGER,
        price REAL,
        status TEXT DEFAULT 'PENDING',
        order_date TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print("  ✅ Orders table created")

conn.commit()

print("\n📦 Adding sample data...")

# Check if products exist
cursor.execute("SELECT COUNT(*) FROM products")
count = cursor.fetchone()[0]

if count == 0:
    print("  → Adding sample products...")
    
    sample_products = [
        ('WH001', 'Wireless Headphones', 'Electronics', 800, 1500, 50, 10, 200),
        ('KB002', 'Mechanical Keyboard', 'Electronics', 1200, 2200, 30, 5, 100),
        ('MS003', 'Gaming Mouse', 'Electronics', 600, 1100, 75, 15, 150),
        ('CH004', 'Phone Charger', 'Accessories', 150, 350, 120, 20, 300),
        ('CS005', 'Phone Case', 'Accessories', 100, 250, 200, 30, 500),
        ('SP006', 'Bluetooth Speaker', 'Electronics', 900, 1800, 40, 10, 100),
        ('CB007', 'USB Cable', 'Accessories', 50, 150, 300, 50, 600),
        ('TB008', 'Tablet Stand', 'Accessories', 300, 650, 60, 15, 150),
    ]
    
    for product in sample_products:
        cursor.execute('''
            INSERT INTO products (sku, name, category, cost_price, selling_price, current_stock, min_stock_level, max_stock_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', product)
        print(f"  ✅ Added: {product[1]}")
    
    conn.commit()
    print(f"\n✅ Added {len(sample_products)} sample products")
else:
    print(f"  ℹ️  Database already has {count} products")

print("\n🎉 Setup Complete!")
print("\n📋 Next Steps:")
print("1. Copy this DATABASE_URL:")
print(f"\n   {DATABASE_URL}\n")
print("2. Add to Vercel:")
print("   → Go to Vercel Dashboard")
print("   → Settings → Environment Variables")
print("   → Add: DATABASE_URL = (paste the URL above)")
print("   → Save and Redeploy")
print("\n3. Your MoonHub is now production-ready! 🚀")

cursor.close()
conn.close()
