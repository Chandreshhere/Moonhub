#!/usr/bin/env python3
"""
Test Supabase Connection
"""

DATABASE_URL = "postgresql://postgres:Onepieceisreal321123@db.xnmrnozypbcufcbwjlgq.supabase.co:5432/postgres"

print("🔍 Testing Supabase Connection...")
print("=" * 60)

try:
    import psycopg2
    print("✅ psycopg2 installed")
except ImportError:
    print("❌ Installing psycopg2...")
    import subprocess
    subprocess.run(["pip", "install", "psycopg2-binary"], check=True)
    import psycopg2

print("\n🔌 Connecting to database...")
print(f"Host: db.xnmrnozypbcufcbwjlgq.supabase.co")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("✅ Connected successfully!")
    
    # Check tables
    print("\n📊 Checking tables...")
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    
    if tables:
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")
            
            # Count rows in each table
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"     ({count} rows)")
    else:
        print("❌ No tables found! Run the SQL script in Supabase.")
    
    # Test adding a product
    print("\n🧪 Testing add product...")
    try:
        cursor.execute("""
            INSERT INTO products (sku, name, category, cost_price, selling_price, current_stock)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, ('TEST999', 'Test Product', 'Test', 100, 200, 50))
        
        product_id = cursor.fetchone()[0]
        conn.commit()
        print(f"✅ Product added successfully! ID: {product_id}")
        
        # Delete test product
        cursor.execute("DELETE FROM products WHERE sku = %s", ('TEST999',))
        conn.commit()
        print("✅ Test product deleted")
        
    except Exception as e:
        print(f"❌ Error adding product: {e}")
        conn.rollback()
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE IS WORKING!")
    print("=" * 60)
    print("\n📋 Next: Add this to Vercel Environment Variables:")
    print(f"\nDATABASE_URL={DATABASE_URL}")
    print("\nThen redeploy!")
    
except Exception as e:
    print(f"\n❌ CONNECTION FAILED!")
    print(f"Error: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Check password is correct: Onepieceisreal321123")
    print("2. Check host is correct: db.xnmrnozypbcufcbwjlgq.supabase.co")
    print("3. Make sure Supabase project is active")
    print("4. Check if you can connect from Supabase dashboard")
