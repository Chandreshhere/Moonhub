#!/usr/bin/env python3
"""
Quick Supabase Setup - Automated
"""

import requests
import json

# Your Supabase details
SUPABASE_URL = "https://your-project.supabase.co"  # Get from Supabase dashboard
SUPABASE_KEY = "sb_secret_O0TP6YILsG9-tpfYCU5cew_uqYrBNr_"  # Your service role key

print("🌙 MoonHub - Quick Supabase Setup")
print("=" * 50)

# You need to provide your Supabase project URL
print("\n📝 To complete setup, I need your Supabase Project URL")
print("\nGet it from:")
print("1. Go to https://supabase.com/dashboard")
print("2. Select your project")
print("3. Go to Settings → API")
print("4. Copy 'Project URL' (looks like: https://xxxxx.supabase.co)")
print("\nOr provide your DATABASE_URL from:")
print("Settings → Database → Connection String → URI")
print("\nExample:")
print("postgresql://postgres:[password]@db.xxxxx.supabase.co:5432/postgres")

print("\n" + "=" * 50)
print("📋 MANUAL SETUP INSTRUCTIONS:")
print("=" * 50)

print("""
STEP 1: Get Your Database URL
------------------------------
1. Go to: https://supabase.com/dashboard
2. Select your project (or create new one)
3. Go to: Settings → Database
4. Scroll to "Connection string"
5. Select "URI" tab
6. Copy the full URL (replace [YOUR-PASSWORD] with actual password)

STEP 2: Add to Vercel
----------------------
1. Go to: https://vercel.com/dashboard
2. Select your "moonhub" project
3. Go to: Settings → Environment Variables
4. Click "Add New"
5. Name: DATABASE_URL
6. Value: (paste your Supabase URL)
7. Select all environments (Production, Preview, Development)
8. Click "Save"

STEP 3: Redeploy
----------------
1. Go to "Deployments" tab
2. Click "..." on latest deployment
3. Click "Redeploy"
4. Wait 2-3 minutes

STEP 4: Initialize Database
----------------------------
Visit your deployed site, it will auto-create tables and sample data!

🎉 Done! Your inventory system is now live with persistent data!
""")

print("\n" + "=" * 50)
print("Need your Supabase Project URL?")
print("Run this command to find it:")
print("\n  Visit: https://supabase.com/dashboard/project/_/settings/api")
print("=" * 50)
