#!/usr/bin/env python3
"""
MoonHub Production Deployment Script
Handles production setup, configuration, and deployment
"""

import os
import sys
import subprocess
import json
import sqlite3
from pathlib import Path

class MoonHubDeployer:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_dir = self.base_dir / 'configs'
        self.logs_dir = self.base_dir / 'logs'
        self.backups_dir = self.base_dir / 'backups'
        
    def setup_directories(self):
        """Create necessary directories for production"""
        print("📁 Setting up directory structure...")
        
        directories = [
            self.config_dir,
            self.logs_dir,
            self.backups_dir,
            self.base_dir / 'exports',
            self.base_dir / 'uploads'
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            print(f"   ✓ Created {directory}")
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing dependencies...")
        
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ], check=True, cwd=self.base_dir)
            print("   ✓ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install dependencies: {e}")
            return False
        return True
    
    def setup_database(self):
        """Initialize production database with sample data"""
        print("🗄️ Setting up production database...")
        
        try:
            from inventory_manager import InventoryManager
            
            # Initialize inventory manager (creates database)
            inventory = InventoryManager()
            
            # Add sample products for production demo
            sample_products = [
                {
                    'sku': 'WH001',
                    'name': 'Wireless Headphones',
                    'category': 'Electronics',
                    'cost_price': 800,
                    'selling_price': 1500,
                    'initial_stock': 45
                },
                {
                    'sku': 'KB002',
                    'name': 'Mechanical Keyboard',
                    'category': 'Electronics',
                    'cost_price': 1200,
                    'selling_price': 2200,
                    'initial_stock': 23
                },
                {
                    'sku': 'MS003',
                    'name': 'Gaming Mouse',
                    'category': 'Electronics',
                    'cost_price': 600,
                    'selling_price': 1100,
                    'initial_stock': 67
                },
                {
                    'sku': 'CH004',
                    'name': 'Phone Charger',
                    'category': 'Accessories',
                    'cost_price': 150,
                    'selling_price': 350,
                    'initial_stock': 120
                },
                {
                    'sku': 'CS005',
                    'name': 'Phone Case',
                    'category': 'Accessories',
                    'cost_price': 100,
                    'selling_price': 250,
                    'initial_stock': 8
                },
                {
                    'sku': 'SP006',
                    'name': 'Bluetooth Speaker',
                    'category': 'Electronics',
                    'cost_price': 900,
                    'selling_price': 1800,
                    'initial_stock': 0
                }
            ]
            
            for product in sample_products:
                try:
                    inventory.add_product(**product)
                    print(f"   ✓ Added product: {product['name']}")
                except:
                    pass  # Product might already exist
            
            print("   ✓ Database setup completed")
            return True
            
        except Exception as e:
            print(f"   ❌ Database setup failed: {e}")
            return False
    
    def create_config_files(self):
        """Create production configuration files"""
        print("⚙️ Creating configuration files...")
        
        # Platform configuration template
        platform_config = {
            "amazon": {
                "name": "Amazon Seller Central",
                "status": "disconnected",
                "credentials": {}
            },
            "flipkart": {
                "name": "Flipkart Seller Hub", 
                "status": "disconnected",
                "credentials": {}
            },
            "meesho": {
                "name": "Meesho Supplier Panel",
                "status": "disconnected", 
                "credentials": {}
            },
            "shopify": {
                "name": "Shopify Store",
                "status": "disconnected",
                "credentials": {}
            },
            "ebay": {
                "name": "eBay Seller Account",
                "status": "disconnected",
                "credentials": {}
            }
        }
        
        # Email configuration template
        email_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "username": "",
            "password": "",
            "recipients": []
        }
        
        # Automation configuration
        automation_config = {
            "stock_sync_interval": 7200,  # 2 hours
            "low_stock_alert_time": "09:00",
            "weekly_report_day": "monday",
            "weekly_report_time": "08:00",
            "backup_time": "23:00"
        }
        
        configs = [
            ('platform_config.json', platform_config),
            ('email_config.json', email_config),
            ('automation_config.json', automation_config)
        ]
        
        for filename, config in configs:
            config_path = self.config_dir / filename
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"   ✓ Created {filename}")
    
    def create_startup_script(self):
        """Create production startup script"""
        print("🚀 Creating startup script...")
        
        startup_script = '''#!/bin/bash
# MoonHub Production Startup Script

echo "🌙 Starting MoonHub Inventory Management System..."

# Set environment variables
export FLASK_ENV=production
export FLASK_APP=web_dashboard.py

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the application with gunicorn for production
echo "🚀 Starting web server on port 8080..."
gunicorn --bind 0.0.0.0:8080 --workers 4 --timeout 120 --log-level info --access-logfile logs/access.log --error-logfile logs/error.log web_dashboard:app

echo "✅ MoonHub started successfully!"
echo "🌐 Access your dashboard at: http://localhost:8080"
'''
        
        startup_path = self.base_dir / 'start_production.sh'
        with open(startup_path, 'w') as f:
            f.write(startup_script)
        
        # Make script executable
        os.chmod(startup_path, 0o755)
        print(f"   ✓ Created startup script: {startup_path}")
    
    def create_systemd_service(self):
        """Create systemd service file for Linux deployment"""
        print("🔧 Creating systemd service file...")
        
        service_content = f'''[Unit]
Description=MoonHub Inventory Management System
After=network.target

[Service]
Type=simple
User=moonhub
WorkingDirectory={self.base_dir}
Environment=PATH={self.base_dir}/venv/bin
ExecStart={self.base_dir}/venv/bin/gunicorn --bind 0.0.0.0:8080 --workers 4 web_dashboard:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
'''
        
        service_path = self.base_dir / 'moonhub.service'
        with open(service_path, 'w') as f:
            f.write(service_content)
        
        print(f"   ✓ Created systemd service: {service_path}")
        print("   📝 To install: sudo cp moonhub.service /etc/systemd/system/")
        print("   📝 To enable: sudo systemctl enable moonhub")
        print("   📝 To start: sudo systemctl start moonhub")
    
    def create_docker_files(self):
        """Create Docker configuration for containerized deployment"""
        print("🐳 Creating Docker configuration...")
        
        dockerfile = '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs configs backups exports uploads

# Expose port
EXPOSE 8080

# Set environment variables
ENV FLASK_ENV=production
ENV FLASK_APP=web_dashboard.py

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "web_dashboard:app"]
'''
        
        docker_compose = '''version: '3.8'

services:
  moonhub:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./configs:/app/configs
      - ./backups:/app/backups
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - moonhub
    restart: unless-stopped
'''
        
        nginx_config = '''events {
    worker_connections 1024;
}

http {
    upstream moonhub {
        server moonhub:8080;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        location / {
            proxy_pass http://moonhub;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
'''
        
        files = [
            ('Dockerfile', dockerfile),
            ('docker-compose.yml', docker_compose),
            ('nginx.conf', nginx_config)
        ]
        
        for filename, content in files:
            with open(self.base_dir / filename, 'w') as f:
                f.write(content)
            print(f"   ✓ Created {filename}")
    
    def deploy(self):
        """Run complete deployment process"""
        print("🌙 MoonHub Production Deployment")
        print("=" * 50)
        
        steps = [
            self.setup_directories,
            self.install_dependencies,
            self.setup_database,
            self.create_config_files,
            self.create_startup_script,
            self.create_systemd_service,
            self.create_docker_files
        ]
        
        for step in steps:
            if not step():
                print(f"❌ Deployment failed at step: {step.__name__}")
                return False
        
        print("\n" + "=" * 50)
        print("✅ MoonHub deployment completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Configure email settings in configs/email_config.json")
        print("2. Add platform API credentials in configs/platform_config.json")
        print("3. Start the application:")
        print("   • Development: python start_server.py")
        print("   • Production: ./start_production.sh")
        print("   • Docker: docker-compose up -d")
        print("\n🌐 Access your dashboard at: http://localhost:8080")
        print("🔐 Default login: admin / admin123")
        
        return True

if __name__ == '__main__':
    deployer = MoonHubDeployer()
    deployer.deploy()