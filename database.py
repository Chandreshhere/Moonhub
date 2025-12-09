"""
Database connection handler - supports both SQLite and PostgreSQL
"""
import os
import sqlite3

# Check if PostgreSQL URL is provided (Supabase)
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL and DATABASE_URL.startswith('postgres'):
    # Use PostgreSQL (Supabase)
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    def get_connection():
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    
    def execute_query(query, params=None, fetch=False):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            conn.close()
            return result
        else:
            conn.commit()
            lastrowid = cursor.lastrowid if hasattr(cursor, 'lastrowid') else None
            conn.close()
            return lastrowid
    
    def setup_database():
        """Initialize PostgreSQL database"""
        conn = get_connection()
        cursor = conn.cursor()
        
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
        
        # Platform listings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS platform_listings (
                id SERIAL PRIMARY KEY,
                product_id INTEGER,
                platform TEXT NOT NULL,
                platform_sku TEXT,
                platform_price REAL,
                stock_allocated INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                last_sync TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Stock movements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_movements (
                id SERIAL PRIMARY KEY,
                product_id INTEGER,
                movement_type TEXT,
                quantity INTEGER,
                platform TEXT,
                order_id TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                order_id TEXT UNIQUE,
                platform TEXT,
                product_id INTEGER,
                quantity INTEGER,
                price REAL,
                status TEXT DEFAULT 'PENDING',
                order_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        conn.commit()
        conn.close()

else:
    # Use SQLite (fallback)
    DB_PATH = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'inventory.db')
    
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    def execute_query(query, params=None, fetch=False):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        
        if fetch:
            result = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return result
        else:
            conn.commit()
            lastrowid = cursor.lastrowid
            conn.close()
            return lastrowid
    
    def setup_database():
        """Initialize SQLite database"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        
        # Platform listings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS platform_listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                platform TEXT NOT NULL,
                platform_sku TEXT,
                platform_price REAL,
                stock_allocated INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                last_sync TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Stock movements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                movement_type TEXT,
                quantity INTEGER,
                platform TEXT,
                order_id TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT UNIQUE,
                platform TEXT,
                product_id INTEGER,
                quantity INTEGER,
                price REAL,
                status TEXT DEFAULT 'PENDING',
                order_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        conn.commit()
        conn.close()
