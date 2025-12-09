"""
Simple SQLite Database Handler
"""
import sqlite3
import os

# Use in-memory database for Vercel serverless
DB_PATH = ':memory:' if os.environ.get('VERCEL') else 'inventory.db'

# Global connection for in-memory database
_connection = None

def get_connection():
    """Get database connection"""
    global _connection
    if DB_PATH == ':memory:':
        if _connection is None:
            _connection = sqlite3.connect(':memory:', check_same_thread=False)
            _connection.row_factory = sqlite3.Row
        return _connection
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def setup_database():
    """Initialize database with tables"""
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Stock movements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            movement_type TEXT,
            quantity INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    conn.commit()
    if DB_PATH != ':memory:':
        conn.close()