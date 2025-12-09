# Vercel Deployment Guide - MoonHub 2025

## Quick Deploy to Vercel

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel**: https://vercel.com
2. **Sign in** with GitHub
3. **Import Project**: Click "Add New" → "Project"
4. **Select Repository**: Choose `Chandreshhere/Moonhub`
5. **Configure Project**:
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Build Command: Leave empty
   - Output Directory: Leave empty
6. **Environment Variables**: Add if needed
7. **Deploy**: Click "Deploy"

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
cd /Users/moon/Documents/inventory
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? moonhub-2025
# - Directory? ./
# - Override settings? No

# Production deployment
vercel --prod
```

## Configuration Files Created

- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless function entry point
- ✅ `requirements.txt` - Python dependencies

## Important Notes

⚠️ **Database Limitation**: Vercel serverless functions are stateless. SQLite won't persist data between requests.

### Solutions:

1. **Use External Database** (Recommended for Production):
   - PostgreSQL (Supabase, Neon, Railway)
   - MongoDB (MongoDB Atlas)
   - MySQL (PlanetScale)

2. **Use Vercel KV Storage**:
   ```bash
   vercel env add KV_REST_API_URL
   vercel env add KV_REST_API_TOKEN
   ```

3. **Deploy to Alternative Platforms**:
   - **Railway**: Full support for SQLite + persistent storage
   - **Render**: Free tier with persistent disk
   - **Fly.io**: Persistent volumes included
   - **Heroku**: Supports SQLite with add-ons

## Alternative: Deploy to Railway (Better for SQLite)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Open in browser
railway open
```

## Post-Deployment

After deployment, your app will be available at:
- Vercel: `https://moonhub-2025.vercel.app`
- Custom domain: Configure in Vercel dashboard

## GitHub Repository

Repository: https://github.com/Chandreshhere/Moonhub
Status: ✅ Updated with mobile responsive design
