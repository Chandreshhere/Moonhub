# 🚀 MoonHub Deployment Guide

## GitHub Setup

### 1. Create GitHub Repository
```bash
# Go to https://github.com/new
# Repository name: moonhub-inventory
# Description: Multi-Platform Inventory Management System
# Public or Private: Your choice
# Don't initialize with README (we already have one)
```

### 2. Push to GitHub
```bash
cd /Users/moon/Documents/inventory

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/moonhub-inventory.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Vercel Deployment

### 1. Sign Up / Login to Vercel
- Go to https://vercel.com
- Sign up with GitHub account
- Authorize Vercel to access your repositories

### 2. Import Project
1. Click "Add New Project"
2. Select "Import Git Repository"
3. Choose your `moonhub-inventory` repository
4. Click "Import"

### 3. Configure Project
- **Framework Preset**: Other
- **Root Directory**: ./
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)

### 4. Environment Variables (Optional)
Add these in Vercel dashboard:
- `FLASK_ENV` = `production`
- `MOONHUB_SECRET_KEY` = `your_random_secret_key`

### 5. Deploy
- Click "Deploy"
- Wait 2-3 minutes for deployment
- Your app will be live at: `https://your-project.vercel.app`

## Important Notes

### Database Limitations
⚠️ Vercel uses serverless functions, which means:
- SQLite database is **ephemeral** (resets on each deployment)
- For production, use external database:
  - **PostgreSQL** (Supabase, Neon, Railway)
  - **MySQL** (PlanetScale, Railway)
  - **MongoDB** (MongoDB Atlas)

### Recommended: Use External Database

#### Option 1: Supabase (PostgreSQL)
```bash
# 1. Sign up at https://supabase.com
# 2. Create new project
# 3. Get connection string
# 4. Add to Vercel environment variables:
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

#### Option 2: MongoDB Atlas
```bash
# 1. Sign up at https://www.mongodb.com/cloud/atlas
# 2. Create free cluster
# 3. Get connection string
# 4. Add to Vercel environment variables:
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/dbname
```

### File Storage
For uploads/exports/backups, use:
- **AWS S3**
- **Cloudinary**
- **Vercel Blob Storage**

## Testing Deployment

### 1. Check Homepage
```bash
curl https://your-project.vercel.app
```

### 2. Check API Endpoints
```bash
curl https://your-project.vercel.app/api/dashboard-stats
```

### 3. Monitor Logs
- Go to Vercel Dashboard
- Select your project
- Click "Logs" tab
- Monitor real-time logs

## Troubleshooting

### Issue: 404 Not Found
- Check `vercel.json` routing configuration
- Ensure `api/index.py` exists
- Redeploy project

### Issue: Module Not Found
- Check `requirements.txt` has all dependencies
- Ensure Python version compatibility
- Check Vercel build logs

### Issue: Database Errors
- SQLite won't persist on Vercel
- Migrate to external database
- Update connection strings

## Custom Domain

### 1. Add Domain in Vercel
- Go to Project Settings
- Click "Domains"
- Add your custom domain
- Follow DNS configuration instructions

### 2. Update DNS Records
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

## Continuous Deployment

Every push to `main` branch will automatically:
1. Trigger new deployment
2. Build and test
3. Deploy to production
4. Update live site

## Support

- **Vercel Docs**: https://vercel.com/docs
- **GitHub Issues**: Create issue in your repository
- **Email**: whoischandresh@gmail.com

---

**🌙 MoonHub - Ready for Production!**
