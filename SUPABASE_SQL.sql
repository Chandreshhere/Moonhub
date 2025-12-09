-- ============================================
-- MoonHub - Supabase Database Setup
-- Run this ENTIRE script in Supabase SQL Editor
-- ============================================

-- 1. DROP existing tables if any (clean start)
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS stock_movements CASCADE;
DROP TABLE IF EXISTS platform_listings CASCADE;
DROP TABLE IF EXISTS products CASCADE;

-- 2. CREATE products table
CREATE TABLE products (
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
);

-- 3. CREATE platform_listings table
CREATE TABLE platform_listings (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    platform_sku TEXT,
    platform_price REAL,
    stock_allocated INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    last_sync TIMESTAMP
);

-- 4. CREATE stock_movements table
CREATE TABLE stock_movements (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    movement_type TEXT,
    quantity INTEGER,
    platform TEXT,
    order_id TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. CREATE orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_id TEXT UNIQUE,
    platform TEXT,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER,
    price REAL,
    status TEXT DEFAULT 'PENDING',
    order_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. INSERT sample products
INSERT INTO products (sku, name, category, cost_price, selling_price, current_stock, min_stock_level, max_stock_level)
VALUES 
    ('WH001', 'Wireless Headphones', 'Electronics', 800, 1500, 50, 10, 200),
    ('KB002', 'Mechanical Keyboard', 'Electronics', 1200, 2200, 30, 5, 100),
    ('MS003', 'Gaming Mouse', 'Electronics', 600, 1100, 75, 15, 150),
    ('CH004', 'Phone Charger', 'Accessories', 150, 350, 120, 20, 300),
    ('CS005', 'Phone Case', 'Accessories', 100, 250, 200, 30, 500),
    ('SP006', 'Bluetooth Speaker', 'Electronics', 900, 1800, 40, 10, 100),
    ('CB007', 'USB Cable', 'Accessories', 50, 150, 300, 50, 600),
    ('TB008', 'Tablet Stand', 'Accessories', 300, 650, 60, 15, 150);

-- 7. Verify tables created
SELECT 'Tables created successfully!' as status;
SELECT COUNT(*) as product_count FROM products;
