#!/usr/bin/env python3
"""
Initialize Supabase Database for MoonHub
"""

import urllib.parse

# Your Supabase credentials
PASSWORD = "@Choice12345"
HOST = "db.ifpdadsvllgxedbgutwt.supabase.co"

# URL encode the password (@ becomes %40)
encoded_password = urllib.parse.quote(PASSWORD, safe='')
DATABASE_URL = f"postgresql://postgres:{encoded_password}@{HOST}:5432/postgres"

print("🌙 MoonHub - Database Initialization")
print("=" * 60)
print(f"\n📋 Your DATABASE_URL (URL-encoded):")
print(f"\n{DATABASE_URL}\n")
print("=" * 60)

try:
    import psycopg2
except ImportError:
    print("\n📦 Installing psycopg2...")
    import os
    os.system("pip install psycopg2-binary")
    import psycopg2

print("\n🔌 Connecting to Supabase...")
try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("✅ Connected successfully!\n")
except Exception as e:
    print(f"❌ Connection failed: {e}\n")
    print("Please add this to Vercel manually:")
    print(f"\nDATABASE_URL={DATABASE_URL}\n")
    exit(1)

print("🗄️  Creating tables...")

# Products table
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
print("  ✅ products")

# Platform listings
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
print("  ✅ platform_listings")

# Stock movements
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
print("  ✅ stock_movements")

# Orders
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
print("  ✅ orders")

conn.commit()

print("\n📦 Adding sample products...")

cursor.execute("SELECT COUNT(*) FROM products")
count = cursor.fetchone()[0]

if count == 0:
    products = [
        ('WH001', 'Wireless Headphones', 'Electronics', 800, 1500, 50, 10, 200),
        ('KB002', 'Mechanical Keyboard', 'Electronics', 1200, 2200, 30, 5, 100),
        ('MS003', 'Gaming Mouse', 'Electronics', 600, 1100, 75, 15, 150),
        ('CH004', 'Phone Charger', 'Accessories', 150, 350, 120, 20, 300),
        ('CS005', 'Phone Case', 'Accessories', 100, 250, 200, 30, 500),
        ('SP006', 'Bluetooth Speaker', 'Electronics', 900, 1800, 40, 10, 100),
        ('CB007', 'USB Cable', 'Accessories', 50, 150, 300, 50, 600),
        ('TB008', 'Tablet Stand', 'Accessories', 300, 650, 60, 15, 150),
    ]
    
    for p in products:
        cursor.execute('''
            INSERT INTO products (sku, name, category, cost_price, selling_price, current_stock, min_stock_level, max_stock_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', p)
        print(f"  ✅ {p[1]}")
    
    conn.commit()
    print(f"\n✅ Added {len(products)} products")
else:
    print(f"  ℹ️  Already have {count} products")

cursor.close()
conn.close()

print("\n" + "=" * 60)
print("🎉 DATABASE SETUP COMPLETE!")
print("=" * 60)

print("\n📋 NEXT STEP: Add to Vercel")
print("\n1. Go to: https://vercel.com/dashboard")
print("2. Select your 'moonhub' project")
print("3. Settings → Environment Variables")
print("4. Add New Variable:")
print(f"\n   Name:  DATABASE_URL")
print(f"   Value: {DATABASE_URL}")
print("\n5. Select all environments (Production, Preview, Development)")
print("6. Click 'Save'")
print("7. Go to Deployments → Redeploy latest")
print("\n🚀 Your MoonHub will be live in 2-3 minutes!")
print("\n" + "=" * 60)
