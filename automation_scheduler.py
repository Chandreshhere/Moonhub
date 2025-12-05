#!/usr/bin/env python3
"""
Automation Scheduler for Inventory Management
Handles automated tasks like stock sync, alerts, and reporting
"""

import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
from datetime import datetime, timedelta
from inventory_manager import InventoryManager, PlatformIntegrator
import logging

class AutomationScheduler:
    def __init__(self, config_file: str = "automation_config.json"):
        self.inventory_manager = InventoryManager()
        self.platform_integrator = PlatformIntegrator(self.inventory_manager)
        self.load_config(config_file)
        self.setup_logging()
    
    def load_config(self, config_file: str):
        """Load automation configuration"""
        try:
            with open(f"/Users/moon/Documents/inventory/{config_file}", 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Default configuration
            self.config = {
                "email": {
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "username": "<your_email@gmail.com>",
                    "password": "<your_app_password>",
                    "recipients": ["<recipient@email.com>"]
                },
                "schedules": {
                    "stock_sync": "every 2 hours",
                    "low_stock_alert": "daily at 09:00",
                    "inventory_report": "weekly on monday at 08:00",
                    "backup": "daily at 23:00"
                },
                "thresholds": {
                    "low_stock_alert_threshold": 10,
                    "critical_stock_threshold": 5
                }
            }
            self.save_config(config_file)
    
    def save_config(self, config_file: str):
        """Save configuration to file"""
        with open(f"/Users/moon/Documents/inventory/{config_file}", 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/Users/moon/Documents/inventory/automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def send_email(self, subject: str, body: str, attachments: list = None):
        """Send email notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['username']
            msg['To'] = ', '.join(self.config['email']['recipients'])
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {file_path.split("/")[-1]}'
                    )
                    msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.config['email']['smtp_server'], self.config['email']['smtp_port'])
            server.starttls()
            server.login(self.config['email']['username'], self.config['email']['password'])
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Email sent: {subject}")
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
    
    def sync_all_platforms(self):
        """Sync inventory across all platforms"""
        self.logger.info("Starting platform sync...")
        
        try:
            self.platform_integrator.sync_amazon_inventory()
            self.platform_integrator.sync_flipkart_inventory()
            self.platform_integrator.sync_meesho_inventory()
            
            self.logger.info("Platform sync completed successfully")
            
        except Exception as e:
            self.logger.error(f"Platform sync failed: {e}")
            self.send_email(
                "Platform Sync Failed",
                f"<h3>Platform Sync Error</h3><p>Error: {str(e)}</p><p>Time: {datetime.now()}</p>"
            )
    
    def check_low_stock_alerts(self):
        """Check for low stock and send alerts"""
        self.logger.info("Checking low stock alerts...")
        
        try:
            low_stock_items = self.inventory_manager.get_low_stock_alerts()
            
            if low_stock_items:
                # Create HTML email body
                html_body = """
                <h2>Low Stock Alert</h2>
                <p>The following items are running low on stock:</p>
                <table border="1" style="border-collapse: collapse;">
                    <tr style="background-color: #f2f2f2;">
                        <th>SKU</th>
                        <th>Product Name</th>
                        <th>Current Stock</th>
                        <th>Minimum Level</th>
                        <th>Action Required</th>
                    </tr>
                """
                
                for item in low_stock_items:
                    priority = "CRITICAL" if item['current_stock'] <= self.config['thresholds']['critical_stock_threshold'] else "LOW"
                    color = "#ffcccc" if priority == "CRITICAL" else "#fff2cc"
                    
                    html_body += f"""
                    <tr style="background-color: {color};">
                        <td>{item['sku']}</td>
                        <td>{item['name']}</td>
                        <td>{item['current_stock']}</td>
                        <td>{item['min_stock_level']}</td>
                        <td>{priority} - Reorder Now</td>
                    </tr>
                    """
                
                html_body += """
                </table>
                <p><strong>Please take immediate action to restock these items.</strong></p>
                """
                
                self.send_email("Low Stock Alert", html_body)
                self.logger.info(f"Low stock alert sent for {len(low_stock_items)} items")
            else:
                self.logger.info("No low stock items found")
                
        except Exception as e:
            self.logger.error(f"Low stock check failed: {e}")
    
    def generate_weekly_report(self):
        """Generate and send weekly inventory report"""
        self.logger.info("Generating weekly inventory report...")
        
        try:
            # Generate Excel report
            report_file = self.inventory_manager.export_to_excel("weekly_inventory_report.xlsx")
            
            # Get summary statistics
            inventory_df = self.inventory_manager.generate_inventory_report()
            total_products = len(inventory_df)
            total_stock_value = (inventory_df['current_stock'] * inventory_df['cost_price']).sum()
            low_stock_count = len(self.inventory_manager.get_low_stock_alerts())
            
            html_body = f"""
            <h2>Weekly Inventory Report</h2>
            <h3>Summary</h3>
            <ul>
                <li><strong>Total Products:</strong> {total_products}</li>
                <li><strong>Total Stock Value:</strong> ₹{total_stock_value:,.2f}</li>
                <li><strong>Low Stock Items:</strong> {low_stock_count}</li>
                <li><strong>Report Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            <p>Detailed inventory report is attached.</p>
            """
            
            self.send_email("Weekly Inventory Report", html_body, [report_file])
            self.logger.info("Weekly report sent successfully")
            
        except Exception as e:
            self.logger.error(f"Weekly report generation failed: {e}")
    
    def backup_database(self):
        """Create database backup"""
        self.logger.info("Creating database backup...")
        
        try:
            import shutil
            backup_filename = f"inventory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = f"/Users/moon/Documents/inventory/backups/{backup_filename}"
            
            # Create backups directory if it doesn't exist
            import os
            os.makedirs("/Users/moon/Documents/inventory/backups", exist_ok=True)
            
            shutil.copy2("/Users/moon/Documents/inventory/inventory.db", backup_path)
            self.logger.info(f"Database backup created: {backup_path}")
            
        except Exception as e:
            self.logger.error(f"Database backup failed: {e}")
    
    def setup_schedules(self):
        """Setup automated schedules"""
        # Stock sync every 2 hours
        schedule.every(2).hours.do(self.sync_all_platforms)
        
        # Low stock alerts daily at 9 AM
        schedule.every().day.at("09:00").do(self.check_low_stock_alerts)
        
        # Weekly report on Monday at 8 AM
        schedule.every().monday.at("08:00").do(self.generate_weekly_report)
        
        # Daily backup at 11 PM
        schedule.every().day.at("23:00").do(self.backup_database)
        
        self.logger.info("Automation schedules configured")
    
    def run_scheduler(self):
        """Run the automation scheduler"""
        self.setup_schedules()
        self.logger.info("Automation scheduler started")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def run_manual_tasks(self):
        """Run all tasks manually for testing"""
        print("Running manual tasks...")
        
        print("1. Syncing platforms...")
        self.sync_all_platforms()
        
        print("2. Checking low stock...")
        self.check_low_stock_alerts()
        
        print("3. Generating report...")
        self.generate_weekly_report()
        
        print("4. Creating backup...")
        self.backup_database()
        
        print("All tasks completed!")

if __name__ == "__main__":
    scheduler = AutomationScheduler()
    
    # For testing, run manual tasks
    # scheduler.run_manual_tasks()
    
    # For production, run the scheduler
    # scheduler.run_scheduler()
    
    print("Automation scheduler ready. Uncomment the desired mode in __main__ section.")