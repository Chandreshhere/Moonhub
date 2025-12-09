# 🚀 Deploy MoonHub to Render.com

## Why Render.com?
✅ Supports numpy/pandas (no size limits)
✅ Persistent SQLite database
✅ Free tier: 750 hours/month
✅ Perfect for Flask apps
✅ Auto-deploy from GitHub

## Quick Deploy (5 Minutes)

### Step 1: Push to GitHub (if not done)
```bash
cd /Users/moon/Documents/inventory
git add .
git commit -m "Add Render deployment config"
git push origin main
```

### Step 2: Deploy on Render

1. Go to **https://render.com**
2. Sign up/login with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your **Moonhub** repository
5. Configure:
   - **Name**: moonhub-inventory
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_dashboard:app`
   - **Instance Type**: Free
6. Click **"Create Web Service"**
7. Wait 5-10 minutes for build ⏳

### Step 3: Access Your App
Your app will be live at:
```
https://moonhub-inventory.onrender.com
```

## ✅ Advantages Over Vercel

| Feature | Render | Vercel |
|---------|--------|--------|
| numpy/pandas | ✅ Works | ⚠️ Size limits |
| SQLite persistence | ✅ Yes | ❌ No |
| Free tier | 750 hrs/month | Serverless limits |
| Flask apps | ✅ Native | ⚠️ Workarounds |

## 🔧 Configuration Files

- `render.yaml` - Render configuration
- `requirements.txt` - Added gunicorn
- `web_dashboard.py` - No changes needed

## ⚠️ Important Notes

### Free Tier Limitations
- Spins down after 15 min of inactivity
- First request after sleep takes ~30 seconds
- 750 hours/month (enough for most use)

### Upgrade to Paid ($7/month)
- Always-on service
- Faster performance
- More resources

## 🎯 Post-Deployment

### Test Your App
```bash
curl https://moonhub-inventory.onrender.com
```

### View Logs
- Go to Render Dashboard
- Select your service
- Click "Logs" tab

### Custom Domain
1. Go to service settings
2. Click "Custom Domain"
3. Add your domain
4. Update DNS records

## 🔄 Auto-Deploy

Every push to GitHub `main` branch will:
1. Trigger automatic deployment
2. Build and test
3. Deploy to production
4. Update live site

## 📊 Monitor Your App

- **Dashboard**: https://dashboard.render.com
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, requests
- **Alerts**: Email notifications

## 🆘 Troubleshooting

### Build Fails?
- Check requirements.txt
- View build logs in Render
- Ensure Python 3.11 compatibility

### App Not Loading?
- Check start command: `gunicorn web_dashboard:app`
- View runtime logs
- Verify port binding (Render auto-assigns)

### Database Issues?
- SQLite persists on Render
- Data survives restarts
- Backup regularly

## 💡 Pro Tips

1. **Keep Free Tier Active**: Visit your app daily
2. **Monitor Usage**: Check dashboard for hours used
3. **Upgrade When Ready**: $7/month for always-on
4. **Use Environment Variables**: For sensitive config

## 🔗 Useful Links

- **Render Docs**: https://render.com/docs
- **Your Dashboard**: https://dashboard.render.com
- **GitHub Repo**: https://github.com/Chandreshhere/Moonhub

---

**🌙 MoonHub on Render - Production Ready!**
