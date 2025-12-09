#!/bin/bash

echo "🌙 MoonHub - GitHub & Vercel Deployment Script"
echo "=============================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
fi

# Get GitHub username
read -p "Enter your GitHub username: " github_username

# Get repository name (default: moonhub-inventory)
read -p "Enter repository name [moonhub-inventory]: " repo_name
repo_name=${repo_name:-moonhub-inventory}

# Create GitHub repository URL
repo_url="https://github.com/$github_username/$repo_name.git"

echo ""
echo "Repository URL: $repo_url"
echo ""

# Check if remote already exists
if git remote | grep -q "origin"; then
    echo "Removing existing remote..."
    git remote remove origin
fi

# Add remote
echo "Adding GitHub remote..."
git remote add origin $repo_url

# Add all files
echo "Adding files to Git..."
git add .

# Commit
echo "Committing changes..."
git commit -m "Deploy MoonHub to GitHub and Vercel" || echo "No changes to commit"

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
echo "You may need to authenticate with GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://vercel.com"
echo "2. Sign in with GitHub"
echo "3. Click 'Add New Project'"
echo "4. Import your repository: $repo_name"
echo "5. Click 'Deploy'"
echo ""
echo "Your app will be live at: https://$repo_name.vercel.app"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT_GUIDE.md"
