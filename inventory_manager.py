"""
Simple Inventory Manager
"""
import sqlite3
from datetime import datetime
from database import get_connection, setup_database
from openpyxl import Workbook
import os

class InventoryManager:
    def __init__(self):
        setup_database()
    
    def add_product(self, sku, name, category, cost_price, selling_price, initial_stock=0):
        """Add new product"""
        try:
            conn = get_connection()
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
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
    
    def update_stock(self, sku, quantity, movement_type='ADJUSTMENT', notes=None):
        """Update stock levels"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Get product
            cursor.execute('SELECT id, current_stock FROM products WHERE sku = ?', (sku,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False
            
            product_id, current_stock = result['id'], result['current_stock']
            
            # Calculate new stock
            if movement_type == 'OUT':
                if current_stock < quantity:
                    conn.close()
                    return False
                new_stock = current_stock - quantity
            else:
                new_stock = current_stock + quantity
            
            # Update stock
            cursor.execute('UPDATE products SET current_stock = ? WHERE id = ?', (new_stock, product_id))
            
            # Record movement
            cursor.execute('''
                INSERT INTO stock_movements (product_id, movement_type, quantity, notes)
                VALUES (?, ?, ?, ?)
            ''', (product_id, movement_type, quantity, notes))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False
    
    def delete_product(self, sku):
        """Delete product"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM products WHERE sku = ?', (sku,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False
            
            product_id = result['id']
            
            # Delete movements first
            cursor.execute('DELETE FROM stock_movements WHERE product_id = ?', (product_id,))
            # Delete product
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
    
    def get_all_products(self):
        """Get all products"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sku, name, category, current_stock, min_stock_level, 
                   cost_price, selling_price
            FROM products
            ORDER BY name
        ''')
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'sku': row['sku'],
                'name': row['name'],
                'category': row['category'],
                'current_stock': row['current_stock'],
                'min_stock_level': row['min_stock_level'],
                'cost_price': row['cost_price'],
                'selling_price': row['selling_price']
            })
        
        conn.close()
        return products
    
    def get_low_stock_alerts(self):
        """Get low stock products"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sku, name, current_stock, min_stock_level
            FROM products
            WHERE current_stock <= min_stock_level
        ''')
        
        alerts = []
        for row in cursor.fetchall():
            alerts.append({
                'sku': row['sku'],
                'name': row['name'],
                'current_stock': row['current_stock'],
                'min_stock_level': row['min_stock_level']
            })
        
        conn.close()
        return alerts
    
    def export_to_excel(self):
        """Export to Excel"""
        try:
            products = self.get_all_products()
            
            wb = Workbook()
            ws = wb.active
            ws.title = "Inventory"
            
            # Headers
            headers = ['SKU', 'Name', 'Category', 'Current Stock', 'Min Stock', 'Cost Price', 'Selling Price']
            ws.append(headers)
            
            # Data
            for product in products:
                ws.append([
                    product['sku'],
                    product['name'],
                    product['category'],
                    product['current_stock'],
                    product['min_stock_level'],
                    product['cost_price'],
                    product['selling_price']
                ])
            
            # Save file
            filename = f"inventory_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = os.path.join('/tmp', filename)
            wb.save(filepath)
            
            return filepath
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return None