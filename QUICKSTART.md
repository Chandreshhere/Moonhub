# 🚀 Quick Start - Deploy MoonHub in 5 Minutes

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `moonhub-inventory`
3. Make it Public or Private
4. **Don't** check "Initialize with README"
5. Click "Create repository"

## Step 2: Push to GitHub

### Option A: Use Automated Script (Easiest)
```bash
cd /Users/moon/Documents/inventory
./deploy_to_github.sh
```
Enter your GitHub username when prompted.

### Option B: Manual Commands
```bash
cd /Users/moon/Documents/inventory

# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/moonhub-inventory.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Vercel

1. **Go to Vercel**: https://vercel.com
2. **Sign in** with GitHub
3. **Click** "Add New Project"
4. **Select** your `moonhub-inventory` repository
5. **Click** "Import"
6. **Click** "Deploy" (use default settings)
7. **Wait** 2-3 minutes ⏳

## Step 4: Access Your App

Your app will be live at:
```
https://moonhub-inventory.vercel.app
```

Or custom URL like:
```
https://your-project-name-abc123.vercel.app
```

## 🎉 That's It!

Your MoonHub Inventory Management System is now live!

## ⚠️ Important Notes

### Database Limitation
- Vercel uses serverless functions
- SQLite database is **temporary** (resets on deployment)
- Data won't persist between deployments

### For Production Use
Migrate to external database:
- **Supabase** (PostgreSQL) - https://supabase.com
- **MongoDB Atlas** - https://mongodb.com/atlas
- **PlanetScale** (MySQL) - https://planetscale.com

## 🔧 Optional: Custom Domain

1. Go to Vercel Dashboard
2. Select your project
3. Settings → Domains
4. Add your domain
5. Update DNS records

## 📊 Monitor Your App

- **Vercel Dashboard**: View logs and analytics
- **GitHub**: Auto-deploys on every push
- **Logs**: Real-time monitoring in Vercel

## 🆘 Need Help?

- Read: `DEPLOYMENT_GUIDE.md` for detailed instructions
- Email: whoischandresh@gmail.com
- GitHub Issues: Create an issue in your repo

---

**🌙 Happy Selling with MoonHub!**
