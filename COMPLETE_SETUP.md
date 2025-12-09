# 🚀 Complete MoonHub Setup - Make Everything Work

## 🎯 Goal: Fix All Errors & Make Website Fully Functional

---

## ⚡ QUICK START (5 Minutes)

### Step 1: Get Your Supabase Database URL

1. **Go to Supabase Dashboard**
   - Visit: https://supabase.com/dashboard
   - Login with your account

2. **Find Your Project**
   - If you don't have a project, click "New Project"
   - Name: `moonhub-inventory`
   - Create a strong password (SAVE IT!)
   - Wait 2 minutes for setup

3. **Get Connection String**
   - Click on your project
   - Go to: **Settings** (⚙️ icon) → **Database**
   - Scroll to **"Connection string"**
   - Click **"URI"** tab
   - You'll see something like:
     ```
     postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
     ```
   - **IMPORTANT**: Replace `[YOUR-PASSWORD]` with your actual password
   - Copy the complete URL

### Step 2: Add Database URL to Vercel

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Select your **moonhub** project

2. **Add Environment Variable**
   - Click **Settings** → **Environment Variables**
   - Click **"Add New"**
   - **Name**: `DATABASE_URL`
   - **Value**: Paste your Supabase URL (from Step 1)
   - **Environments**: Check all 3 boxes (Production, Preview, Development)
   - Click **"Save"**

3. **Redeploy**
   - Go to **Deployments** tab
   - Find latest deployment
   - Click **"..."** (three dots)
   - Click **"Redeploy"**
   - Wait 2-3 minutes ⏳

### Step 3: Initialize Database

**Option A: Automatic (Recommended)**
- Just visit your Vercel URL
- The app will auto-create tables and sample data
- Refresh the page - you should see products!

**Option B: Manual SQL Setup**
1. Go to Supabase Dashboard → **SQL Editor**
2. Click **"New query"**
3. Paste this SQL:

```sql
-- Create products table
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
);

-- Create platform_listings table
CREATE TABLE IF NOT EXISTS platform_listings (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    platform_sku TEXT,
    platform_price REAL,
    stock_allocated INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    last_sync TIMESTAMP
);

-- Create stock_movements table
CREATE TABLE IF NOT EXISTS stock_movements (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    movement_type TEXT,
    quantity INTEGER,
    platform TEXT,
    order_id TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create orders table
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
);

-- Insert sample products
INSERT INTO products (sku, name, category, cost_price, selling_price, current_stock, min_stock_level, max_stock_level)
VALUES 
    ('WH001', 'Wireless Headphones', 'Electronics', 800, 1500, 50, 10, 200),
    ('KB002', 'Mechanical Keyboard', 'Electronics', 1200, 2200, 30, 5, 100),
    ('MS003', 'Gaming Mouse', 'Electronics', 600, 1100, 75, 15, 150),
    ('CH004', 'Phone Charger', 'Accessories', 150, 350, 120, 20, 300),
    ('CS005', 'Phone Case', 'Accessories', 100, 250, 200, 30, 500),
    ('SP006', 'Bluetooth Speaker', 'Electronics', 900, 1800, 40, 10, 100),
    ('CB007', 'USB Cable', 'Accessories', 50, 150, 300, 50, 600),
    ('TB008', 'Tablet Stand', 'Accessories', 300, 650, 60, 15, 150)
ON CONFLICT (sku) DO NOTHING;
```

4. Click **"Run"**
5. You should see: "Success. No rows returned"

---

## ✅ Verify Everything Works

### Test Checklist:

1. **Dashboard Loads** ✓
   - Visit your Vercel URL
   - Should see dashboard with stats
   - Should see 8 sample products

2. **Add Product** ✓
   - Click "Add Product" button
   - Fill in details
   - Click "Add Product"
   - Should see success message
   - Product appears in table

3. **Update Stock** ✓
   - Click "Update Stock" button
   - Enter SKU (e.g., WH001)
   - Select movement type
   - Enter quantity
   - Click "Update Stock"
   - Stock quantity changes in table

4. **Delete Product** ✓
   - Click trash icon on any product
   - Confirm deletion
   - Product disappears from table

5. **Data Persists** ✓
   - Add a product
   - Refresh page
   - Product still there!
   - Close browser, come back later
   - Data still there!

6. **Excel Export** ✓
   - Click "Export" in navbar
   - Excel file downloads
   - Open file - see all products

7. **Reports Page** ✓
   - Click "Reports" in navbar
   - See analytics and charts

8. **Platforms Page** ✓
   - Click "Platforms" in navbar
   - See platform connections

9. **Admin Page** ✓
   - Click "Admin" dropdown
   - Click "Admin Settings"
   - See admin panel

---

## 🐛 Troubleshooting

### Error: "Product not found" when updating stock
**Fix**: Make sure you're using the exact SKU (case-sensitive)
- Check the SKU in the products table
- Copy-paste it to avoid typos

### Error: "Failed to add product"
**Fix**: SKU must be unique
- Try a different SKU
- Check if product already exists

### Error: "Connection failed"
**Fix**: Check DATABASE_URL
1. Verify it's set in Vercel environment variables
2. Make sure password is correct (no [YOUR-PASSWORD] placeholder)
3. Redeploy after adding/changing environment variable

### Data keeps disappearing
**Fix**: DATABASE_URL not set
- Without DATABASE_URL, app uses SQLite (temporary)
- Add DATABASE_URL to Vercel (see Step 2 above)
- Redeploy

### Page shows "500 Internal Server Error"
**Fix**: Check Vercel logs
1. Go to Vercel Dashboard → Your Project
2. Click "Logs" tab
3. Look for error messages
4. Usually means DATABASE_URL is missing or incorrect

### Excel export doesn't work
**Fix**: This is normal on Vercel
- Vercel serverless functions have limited file system access
- Excel export works but file is temporary
- For production, consider storing exports in cloud storage (S3, Cloudinary)

---

## 🎯 What Should Work Now

### ✅ Fully Functional Features:

1. **Dashboard**
   - Real-time stats (products, stock value, low stock, profit margin)
   - Product inventory table
   - Search and filter products
   - Auto-refresh every 30 seconds

2. **Product Management**
   - Add new products
   - Update stock levels (IN/OUT/ADJUSTMENT)
   - Delete products
   - View all product details

3. **Data Persistence**
   - All changes saved to Supabase
   - Data survives deployments
   - Multi-user support
   - Real-time updates

4. **Reports & Analytics**
   - Sales reports
   - Inventory valuation
   - Platform performance
   - Excel exports

5. **Platform Integration**
   - Connect Amazon, Flipkart, Meesho, Shopify, eBay
   - API configuration
   - Sync status

6. **Admin Panel**
   - System settings
   - User management
   - Configuration

---

## 📊 Database Structure

Your Supabase database now has:

### Tables:
1. **products** - Main inventory (SKU, name, prices, stock)
2. **platform_listings** - Platform-specific listings
3. **stock_movements** - Stock change history
4. **orders** - Order tracking

### Sample Data:
- 8 products across Electronics & Accessories
- Various stock levels (some low, some high)
- Different price points

---

## 🔐 Security

### Your Data is Secure:
- ✅ SSL encrypted connections
- ✅ Password protected database
- ✅ Environment variables (not in code)
- ✅ Service role key for admin access
- ✅ Row-level security (can be enabled)

### Best Practices:
- Never commit DATABASE_URL to git
- Use Vercel environment variables only
- Rotate passwords periodically
- Enable Supabase RLS for production

---

## 📈 Monitor Your System

### Supabase Dashboard:
- **Table Editor**: View/edit data directly
- **SQL Editor**: Run custom queries
- **Database**: Check storage usage
- **Logs**: See database activity

### Vercel Dashboard:
- **Deployments**: See deployment history
- **Logs**: View application logs
- **Analytics**: Track usage
- **Environment Variables**: Manage config

---

## 🎉 Success Criteria

Your MoonHub is fully working when:

✅ Dashboard loads without errors  
✅ Can add products (they appear in table)  
✅ Can update stock (numbers change)  
✅ Can delete products (they disappear)  
✅ Data persists after refresh  
✅ Data persists after closing browser  
✅ Data persists after Vercel redeploy  
✅ Multiple users see same data  
✅ Reports page loads  
✅ Platforms page loads  
✅ Admin page loads  
✅ Excel export downloads  

---

## 🆘 Still Having Issues?

### Check These:

1. **Vercel Environment Variables**
   ```
   DATABASE_URL = postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
   ```
   - Must be set in Vercel
   - Must have real password (not [YOUR-PASSWORD])
   - Must be in all environments

2. **Supabase Tables**
   - Run the SQL from Step 3 Option B
   - Check Table Editor - should see 4 tables
   - Check products table - should have 8 rows

3. **Vercel Deployment**
   - Must redeploy after adding DATABASE_URL
   - Check deployment logs for errors
   - Latest deployment should be successful (green checkmark)

4. **Browser Console**
   - Open browser DevTools (F12)
   - Check Console tab for JavaScript errors
   - Check Network tab for failed API calls

---

## 📞 Support

- **Supabase Docs**: https://supabase.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **GitHub Issues**: Create issue in your repo

---

**🌙 MoonHub - Production Ready Inventory System**

Your inventory management system is now fully functional with:
- ✅ Persistent PostgreSQL database
- ✅ Real-time updates
- ✅ Multi-platform support
- ✅ Automated workflows
- ✅ Professional dashboard
- ✅ Complete CRUD operations

**Happy Selling! 🚀**
