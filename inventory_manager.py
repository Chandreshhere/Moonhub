#!/usr/bin/env python3
"""
Multi-Platform Inventory Management System
Supports Amazon, Flipkart, Meesho, and other platforms
"""

import json
import sqlite3
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Optional
import logging
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

class InventoryManager:
    def __init__(self, db_path: str = "inventory.db"):
        self.db_path = db_path
        self.setup_database()
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('inventory.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            )
        ''')
        
        # Platform listings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS platform_listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                platform TEXT NOT NULL,
                platform_sku TEXT,
                platform_price REAL,
                stock_allocated INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                last_sync TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Stock movements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                movement_type TEXT, -- 'IN', 'OUT', 'ADJUSTMENT'
                quantity INTEGER,
                platform TEXT,
                order_id TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT UNIQUE,
                platform TEXT,
                product_id INTEGER,
                quantity INTEGER,
                price REAL,
                status TEXT DEFAULT 'PENDING',
                order_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_product(self, sku: str, name: str, category: str, cost_price: float, 
                   selling_price: float, initial_stock: int = 0) -> bool:
        """Add new product to inventory"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO products (sku, name, category, cost_price, selling_price, current_stock)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (sku, name, category, cost_price, selling_price, initial_stock))
            
            product_id = cursor.lastrowid
            
            if initial_stock > 0:
                cursor.execute('''
                    INSERT INTO stock_movements (product_id, movement_type, quantity, notes)
                    VALUES (?, 'IN', ?, 'Initial stock')
                ''', (product_id, initial_stock))
            
            conn.commit()
            conn.close()
            self.logger.info(f"Product {sku} added successfully")
            return True
            
        except sqlite3.IntegrityError:
            self.logger.error(f"Product with SKU {sku} already exists")
            return False
        except Exception as e:
            self.logger.error(f"Error adding product: {e}")
            return False
    
    def update_stock(self, sku: str, quantity: int, movement_type: str = 'ADJUSTMENT', 
                    platform: str = None, order_id: str = None, notes: str = None) -> bool:
        """Update stock levels"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get product ID and current stock
            cursor.execute('SELECT id, current_stock FROM products WHERE sku = ?', (sku,))
            result = cursor.fetchone()
            
            if not result:
                self.logger.error(f"Product {sku} not found")
                return False
            
            product_id, current_stock = result
            
            if movement_type == 'OUT' and current_stock < quantity:
                self.logger.error(f"Insufficient stock for {sku}. Available: {current_stock}, Required: {quantity}")
                return False
            
            # Calculate new stock
            if movement_type == 'IN' or movement_type == 'ADJUSTMENT':
                new_stock = current_stock + quantity
            else:  # OUT
                new_stock = current_stock - quantity
            
            # Update product stock
            cursor.execute('''
                UPDATE products SET current_stock = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (new_stock, product_id))
            
            # Record movement
            cursor.execute('''
                INSERT INTO stock_movements (product_id, movement_type, quantity, platform, order_id, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (product_id, movement_type, quantity, platform, order_id, notes))
            
            conn.commit()
            conn.close()
            self.logger.info(f"Stock updated for {sku}: {current_stock} -> {new_stock}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating stock: {e}")
            return False
    
    def add_platform_listing(self, sku: str, platform: str, platform_sku: str, 
                           platform_price: float, stock_allocated: int = 0) -> bool:
        """Add product listing to a platform"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM products WHERE sku = ?', (sku,))
            result = cursor.fetchone()
            
            if not result:
                self.logger.error(f"Product {sku} not found")
                return False
            
            product_id = result[0]
            
            cursor.execute('''
                INSERT INTO platform_listings (product_id, platform, platform_sku, platform_price, stock_allocated)
                VALUES (?, ?, ?, ?, ?)
            ''', (product_id, platform, platform_sku, platform_price, stock_allocated))
            
            conn.commit()
            conn.close()
            self.logger.info(f"Platform listing added: {sku} on {platform}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding platform listing: {e}")
            return False
    
    def get_low_stock_alerts(self) -> List[Dict]:
        """Get products with stock below minimum level"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sku, name, current_stock, min_stock_level
            FROM products
            WHERE current_stock <= min_stock_level
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'sku': row[0],
                'name': row[1],
                'current_stock': row[2],
                'min_stock_level': row[3]
            }
            for row in results
        ]
    
    def generate_inventory_report(self) -> List[Dict]:
        """Generate comprehensive inventory report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                p.sku,
                p.name,
                p.category,
                p.current_stock,
                p.min_stock_level,
                p.cost_price,
                p.selling_price,
                COUNT(pl.id) as platform_count,
                GROUP_CONCAT(pl.platform) as platforms
            FROM products p
            LEFT JOIN platform_listings pl ON p.id = pl.product_id
            GROUP BY p.id
        '''
        
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def export_to_excel(self, filename: str = None) -> str:
        """Export inventory data to Excel"""
        if not filename:
            filename = f"inventory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        filepath = filename
        
        wb = Workbook()
        wb.remove(wb.active)
        
        # Main inventory report
        ws1 = wb.create_sheet('Inventory')
        inventory_data = self.generate_inventory_report()
        if inventory_data:
            headers = list(inventory_data[0].keys())
            ws1.append(headers)
            for row in inventory_data:
                ws1.append([row[h] for h in headers])
        
        # Low stock alerts
        ws2 = wb.create_sheet('Low Stock Alerts')
        low_stock = self.get_low_stock_alerts()
        if low_stock:
            headers = list(low_stock[0].keys())
            ws2.append(headers)
            for row in low_stock:
                ws2.append([row[h] for h in headers])
        
        # Platform listings
        ws3 = wb.create_sheet('Platform Listings')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                p.sku,
                p.name,
                pl.platform,
                pl.platform_sku,
                pl.platform_price,
                pl.stock_allocated,
                pl.is_active
            FROM products p
            JOIN platform_listings pl ON p.id = pl.product_id
        ''')
        columns = [desc[0] for desc in cursor.description]
        ws3.append(columns)
        for row in cursor.fetchall():
            ws3.append(row)
        conn.close()
        
        wb.save(filepath)
        self.logger.info(f"Excel report exported: {filepath}")
        return filepath

# Platform-specific integrations (mock implementations)
class PlatformIntegrator:
    def __init__(self, inventory_manager: InventoryManager):
        self.inventory_manager = inventory_manager
        self.load_platform_configs()
    
    def load_platform_configs(self):
        """Load platform API configurations"""
        try:
            with open('/Users/moon/Documents/inventory/platform_config.json', 'r') as f:
                self.configs = json.load(f)
        except FileNotFoundError:
            self.configs = {}
    
    def sync_amazon_inventory(self):
        """Sync inventory with Amazon (mock implementation)"""
        # This would integrate with Amazon MWS/SP-API
        self.inventory_manager.logger.info("Amazon inventory sync completed")
    
    def sync_flipkart_inventory(self):
        """Sync inventory with Flipkart (mock implementation)"""
        # This would integrate with Flipkart API
        self.inventory_manager.logger.info("Flipkart inventory sync completed")
    
    def sync_meesho_inventory(self):
        """Sync inventory with Meesho (mock implementation)"""
        # This would integrate with Meesho API
        self.inventory_manager.logger.info("Meesho inventory sync completed")

if __name__ == "__main__":
    # Example usage
    inventory = InventoryManager()
    
    # Add sample products
    inventory.add_product("SKU001", "Wireless Headphones", "Electronics", 500, 1200, 50)
    inventory.add_product("SKU002", "Phone Case", "Accessories", 50, 200, 100)
    
    # Add platform listings
    inventory.add_platform_listing("SKU001", "Amazon", "AMZN-WH001", 1199, 20)
    inventory.add_platform_listing("SKU001", "Flipkart", "FK-WH001", 1150, 15)
    
    # Generate report
    report_file = inventory.export_to_excel()
    print(f"Inventory report generated: {report_file}")