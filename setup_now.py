#!/usr/bin/env python3
"""
Setup MoonHub Database - Run this now!
"""

# Your correct DATABASE_URL with encoded password
# @ symbol is encoded as %40
DATABASE_URL = "postgresql://postgres:%40Choice12345@db.xnmrnozypbcufcbwjlgq.supabase.co:5432/postgres"

print("🌙 MoonHub - Database Setup")
print("=" * 70)

try:
    import psycopg2
except ImportError:
    print("📦 Installing psycopg2...")
    import subprocess
    subprocess.run(["pip", "install", "psycopg2-binary"], check=True)
    import psycopg2

print("\n🔌 Connecting to Supabase...")
try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("✅ Connected successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print("\n🗄️  Creating tables...")

# Create all tables
tables = [
    ("products", '''
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
    '''),
    ("platform_listings", '''
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
    '''),
    ("stock_movements", '''
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
    '''),
    ("orders", '''
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
]

for name, sql in tables:
    cursor.execute(sql)
    print(f"  ✅ {name}")

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
    print(f"\n✅ Added {len(products)} products!")
else:
    print(f"  ℹ️  Database already has {count} products")

cursor.close()
conn.close()

print("\n" + "=" * 70)
print("🎉 DATABASE READY!")
print("=" * 70)

print("\n📋 FINAL STEP: Add to Vercel Environment Variables")
print("\n1. Go to: https://vercel.com/dashboard")
print("2. Select your 'moonhub' project")
print("3. Settings → Environment Variables → Add New")
print("\n4. Copy and paste this:")
print("\n   Name:  DATABASE_URL")
print(f"   Value: {DATABASE_URL}")
print("\n5. Check all 3 environments (Production, Preview, Development)")
print("6. Click 'Save'")
print("7. Deployments tab → Click '...' → Redeploy")
print("\n🚀 Your MoonHub will be fully functional in 2-3 minutes!")
print("\n✅ All features will work:")
print("   • Add/Update/Delete products")
print("   • Data persists forever")
print("   • Real-time updates")
print("   • Excel exports")
print("   • All pages working")
print("\n" + "=" * 70)
