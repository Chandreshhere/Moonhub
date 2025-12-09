# 🗄️ Supabase Database Setup for MoonHub

## Why Supabase?
✅ **Persistent Data** - Data survives deployments  
✅ **PostgreSQL** - Powerful relational database  
✅ **Free Tier** - 500MB database, perfect for inventory  
✅ **Auto-backups** - Daily backups included  
✅ **Real-time** - Live data updates  

## Quick Setup (5 Minutes)

### Step 1: Create Supabase Account
1. Go to **https://supabase.com**
2. Click **"Start your project"**
3. Sign up with GitHub (recommended)

### Step 2: Create New Project
1. Click **"New Project"**
2. **Name**: moonhub-inventory
3. **Database Password**: Create a strong password (save it!)
4. **Region**: Choose closest to you
5. Click **"Create new project"**
6. Wait 2-3 minutes for setup ⏳

### Step 3: Get Database URL
1. In your project, go to **Settings** (gear icon)
2. Click **"Database"** in sidebar
3. Scroll to **"Connection string"**
4. Select **"URI"** tab
5. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```
6. Replace `[YOUR-PASSWORD]` with your actual password

### Step 4: Add to Vercel
1. Go to **https://vercel.com/dashboard**
2. Select your **moonhub** project
3. Go to **Settings** → **Environment Variables**
4. Add new variable:
   - **Name**: `DATABASE_URL`
   - **Value**: Your Supabase connection string
   - **Environment**: Production, Preview, Development (select all)
5. Click **"Save"**

### Step 5: Redeploy
1. Go to **Deployments** tab
2. Click **"..."** on latest deployment
3. Click **"Redeploy"**
4. Wait 2-3 minutes ⏳

## ✅ Done! Your Data is Now Persistent!

### Test It:
1. Visit your Vercel URL
2. Add a product
3. Refresh the page
4. Product should still be there! 🎉

## 📊 View Your Data

### In Supabase Dashboard:
1. Go to **Table Editor** in sidebar
2. You'll see tables:
   - `products` - All your inventory
   - `stock_movements` - Stock history
   - `platform_listings` - Platform connections
   - `orders` - Order history

### Run SQL Queries:
1. Go to **SQL Editor**
2. Try:
   ```sql
   SELECT * FROM products;
   SELECT * FROM stock_movements ORDER BY created_at DESC LIMIT 10;
   ```

## 🔒 Security

### Database is Secure:
- ✅ SSL encrypted connections
- ✅ Password protected
- ✅ Only your Vercel app can access
- ✅ Daily backups

### Best Practices:
- Never share your DATABASE_URL
- Use environment variables only
- Rotate password periodically

## 📈 Monitor Usage

### Check Database Size:
1. Supabase Dashboard → **Settings** → **Database**
2. See storage used
3. Free tier: 500MB (plenty for inventory!)

### Upgrade if Needed:
- Free: 500MB, 2GB bandwidth
- Pro: $25/month, 8GB database, 50GB bandwidth

## 🆘 Troubleshooting

### Connection Error?
- Check DATABASE_URL is correct
- Ensure password has no special characters that need escaping
- Verify Vercel environment variable is set

### Data Not Persisting?
- Confirm DATABASE_URL environment variable exists
- Check Vercel logs for errors
- Redeploy after adding environment variable

### Slow Queries?
- Supabase free tier is fast enough
- If needed, upgrade to Pro for better performance

## 🎯 What Happens Now?

### With Supabase:
✅ Add products → They stay forever  
✅ Update stock → Changes persist  
✅ Delete products → Removed permanently  
✅ Export Excel → Real data  
✅ Multi-user → Everyone sees same data  

### Without Supabase (SQLite):
❌ Data resets on each deployment  
❌ Changes lost after 15 min  
❌ Not suitable for production  

## 📞 Support

- **Supabase Docs**: https://supabase.com/docs
- **Supabase Discord**: https://discord.supabase.com
- **MoonHub Issues**: Create issue on GitHub

---

**🌙 MoonHub + Supabase = Production Ready!**
