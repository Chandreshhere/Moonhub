# 🚀 Complete Setup Instructions - Make MoonHub Work

## ⚡ STEP 1: Setup Supabase Database (5 minutes)

### 1.1 Go to Supabase SQL Editor
1. Open: **https://supabase.com/dashboard**
2. Select your project
3. Click **"SQL Editor"** in left sidebar
4. Click **"New query"** button

### 1.2 Run This SQL Script
Copy and paste this ENTIRE script, then click **"Run"**:

```sql
-- DROP existing tables (clean start)
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS stock_movements CASCADE;
DROP TABLE IF EXISTS platform_listings CASCADE;
DROP TABLE IF EXISTS products CASCADE;

-- CREATE products table
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

-- CREATE platform_listings table
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

-- CREATE stock_movements table
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

-- CREATE orders table
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

-- INSERT sample products
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
```

### 1.3 Verify Tables Created
After running the script, you should see:
- ✅ "Success. No rows returned" message
- Go to **Table Editor** in left sidebar
- You should see 4 tables: `products`, `platform_listings`, `stock_movements`, `orders`
- Click on `products` table - should see 8 rows

---

## ⚡ STEP 2: Add DATABASE_URL to Vercel (2 minutes)

### 2.1 Go to Vercel Dashboard
1. Open: **https://vercel.com/dashboard**
2. Click on your **moonhub** project

### 2.2 Add Environment Variable
1. Click **"Settings"** (top menu)
2. Click **"Environment Variables"** (left sidebar)
3. Click **"Add New"** button

### 2.3 Enter These Values:

**Name:**
```
DATABASE_URL
```

**Value:**
```
postgresql://postgres:%40Choice12345@db.xnmrnozypbcufcbwjlgq.supabase.co:5432/postgres
```

**Environments:** (Check ALL 3 boxes)
- ✅ Production
- ✅ Preview
- ✅ Development

4. Click **"Save"**

---

## ⚡ STEP 3: Redeploy on Vercel (1 minute)

1. Go to **"Deployments"** tab (top menu)
2. Find the latest deployment (top of list)
3. Click the **"..."** (three dots) button
4. Click **"Redeploy"**
5. Wait 2-3 minutes for deployment to complete
6. Look for green checkmark ✅

---

## ⚡ STEP 4: Test Your Website (2 minutes)

### 4.1 Visit Your Site
Go to your Vercel URL (something like: `https://moonhub-xxx.vercel.app`)

### 4.2 Check Dashboard
You should see:
- ✅ Dashboard loads without errors
- ✅ Stats showing: 8 products, stock value, etc.
- ✅ Table showing 8 sample products

### 4.3 Test Add Product
1. Click **"Add Product"** button
2. Modal should appear centered (not hidden)
3. Fill in:
   - SKU: `TEST001`
   - Name: `Test Product`
   - Category: `Test`
   - Cost Price: `100`
   - Selling Price: `200`
   - Initial Stock: `50`
4. Click **"Add Product"**
5. Should see success popup
6. Product appears in table

### 4.4 Test Update Stock
1. Click **"Update Stock"** button
2. Fill in:
   - SKU: `TEST001`
   - Movement Type: `IN`
   - Quantity: `10`
3. Click **"Update Stock"**
4. Stock should change from 50 to 60

### 4.5 Test Delete
1. Click trash icon on TEST001 product
2. Confirm deletion
3. Product disappears from table

### 4.6 Test Export
1. Click **"Export"** in navbar
2. Excel file should download
3. Open file - should see all products

---

## 🐛 Troubleshooting

### Problem: "Database not initialized" error

**Solution:**
1. Check if DATABASE_URL is set in Vercel:
   - Vercel → Settings → Environment Variables
   - Should see `DATABASE_URL` listed
2. If not there, add it (see Step 2)
3. Redeploy (see Step 3)

### Problem: Tables not showing in Supabase

**Solution:**
1. Go to Supabase → SQL Editor
2. Run this to check:
   ```sql
   SELECT table_name FROM information_schema.tables 
   WHERE table_schema = 'public';
   ```
3. Should see: products, platform_listings, stock_movements, orders
4. If not, run the full SQL script again (Step 1.2)

### Problem: "Product already exists" when adding

**Solution:**
- Each SKU must be unique
- Try a different SKU like TEST002, TEST003, etc.

### Problem: Can't update stock - "Product not found"

**Solution:**
- SKU is case-sensitive
- Copy the exact SKU from the table
- Make sure product exists in database

### Problem: Modal still hidden under navbar

**Solution:**
1. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Clear browser cache
3. Try incognito/private window

### Problem: Export not working

**Solution:**
1. Check browser popup blocker
2. Allow downloads from your site
3. Check Downloads folder
4. Try different browser

---

## ✅ Success Checklist

Your MoonHub is working when:

- ✅ Dashboard loads with 8 products
- ✅ Can add new products
- ✅ Can update stock quantities
- ✅ Can delete products
- ✅ Modals appear centered
- ✅ Excel export downloads
- ✅ Data persists after refresh
- ✅ No error messages

---

## 📊 Verify Database

### Check in Supabase:
1. Go to **Table Editor**
2. Click **products** table
3. Should see all your products
4. Try adding a product in your app
5. Refresh Supabase - new product should appear

### Check in Vercel:
1. Go to **Logs** tab
2. Should see: "✅ Inventory Manager initialized"
3. No error messages about database connection

---

## 🎯 What to Do Next

1. **Delete sample products** if you don't need them
2. **Add your real products** with actual SKUs and prices
3. **Set up platform connections** (Amazon, Flipkart, etc.)
4. **Customize categories** for your business
5. **Start managing inventory!**

---

## 📞 Still Not Working?

### Check These 3 Things:

1. **Supabase Tables**
   - Go to Supabase → Table Editor
   - Should see 4 tables with data

2. **Vercel Environment Variable**
   - Go to Vercel → Settings → Environment Variables
   - DATABASE_URL should be there
   - Value should start with: `postgresql://postgres:%40Choice12345@`

3. **Vercel Deployment**
   - Go to Vercel → Deployments
   - Latest deployment should have green checkmark ✅
   - Check logs for errors

If all 3 are correct and it still doesn't work:
- Try redeploying one more time
- Wait 5 minutes for changes to propagate
- Clear browser cache and try again

---

**🌙 MoonHub - Ready to Use!**

Follow these steps exactly and your inventory system will work perfectly! 🚀
