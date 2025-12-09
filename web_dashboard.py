#!/usr/bin/env python3
"""
Web Dashboard for Inventory Management
Flask-based web interface for real-time inventory monitoring
"""

from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from flask_cors import CORS
import json
from datetime import datetime, timedelta
from inventory_manager import InventoryManager
import os
import requests
import random
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection

app = Flask(__name__)
app.secret_key = 'moonhub_production_key_2024'
CORS(app)

# Initialize inventory manager
inventory_manager = None
try:
    inventory_manager = InventoryManager()
    print("✅ Inventory Manager initialized")
    # Add sample data if empty
    try:
        inventory_data = inventory_manager.generate_inventory_report()
        if len(inventory_data) == 0:
            inventory_manager.add_product("SKU001", "Wireless Headphones", "Electronics", 500, 1200, 50)
            inventory_manager.add_product("SKU002", "Phone Case", "Accessories", 50, 200, 100)
            inventory_manager.add_product("SKU003", "USB Cable", "Electronics", 30, 150, 200)
            print("✅ Sample data added")
    except Exception as e:
        print(f"Warning: Could not add sample data: {e}")
except Exception as e:
    print(f"❌ Error initializing inventory: {e}")
    # Create a dummy manager to prevent None errors
    class DummyManager:
        def generate_inventory_report(self):
            return []
        def get_low_stock_alerts(self):
            return []
        def add_product(self, *args, **kwargs):
            return False
        def update_stock(self, *args, **kwargs):
            return False
        def export_to_excel(self, *args, **kwargs):
            return None
    inventory_manager = DummyManager()

# Platform API configurations
PLATFORM_CONFIGS = {
    'amazon': {'name': 'Amazon', 'status': 'disconnected'},
    'flipkart': {'name': 'Flipkart', 'status': 'disconnected'},
    'meesho': {'name': 'Meesho', 'status': 'disconnected'},
    'shopify': {'name': 'Shopify', 'status': 'disconnected'},
    'ebay': {'name': 'eBay', 'status': 'disconnected'}
}

@app.route('/')
def login():
    """Login page"""
    try:
        return send_file('login.html')
    except:
        return '<h1>🌙 MoonHub Inventory System</h1><p>Dashboard: <a href="/dashboard">/dashboard</a></p><p>API: <a href="/api/dashboard-stats">/api/dashboard-stats</a></p>'

@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/admin')
def admin():
    """Admin panel page"""
    return render_template('admin.html')

@app.route('/reports')
def reports():
    """Reports and analytics page"""
    return render_template('reports.html')

@app.route('/platforms')
def platforms():
    """Platform management page"""
    return render_template('platforms.html')

@app.route('/api/dashboard-stats')
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        if not inventory_manager:
            return jsonify({'error': 'Database not initialized'}), 500
        
        # Get inventory data
        inventory_data = inventory_manager.generate_inventory_report()
        low_stock_items = inventory_manager.get_low_stock_alerts()
        
        # Calculate statistics
        total_products = len(inventory_data)
        total_stock_value = sum(item['current_stock'] * item['cost_price'] for item in inventory_data)
        low_stock_count = len(low_stock_items)
        out_of_stock_count = sum(1 for item in inventory_data if item['current_stock'] == 0)
        
        profit_margins = [(item['selling_price'] - item['cost_price']) / item['selling_price'] * 100 
                         for item in inventory_data if item['selling_price'] > 0]
        avg_profit_margin = sum(profit_margins) / len(profit_margins) if profit_margins else 0
        
        return jsonify({
            'total_products': total_products,
            'total_stock_value': round(total_stock_value, 2),
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'avg_profit_margin': round(avg_profit_margin, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inventory-data')
def get_inventory_data():
    """Get inventory data for table display"""
    try:
        if not inventory_manager:
            return jsonify({'error': 'Database not initialized'}), 500
        
        inventory_data = inventory_manager.generate_inventory_report()
        return jsonify(inventory_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/low-stock-alerts')
def get_low_stock_alerts():
    """Get low stock alerts"""
    try:
        if not inventory_manager:
            return jsonify({'error': 'Database not initialized'}), 500
        
        alerts = inventory_manager.get_low_stock_alerts()
        return jsonify(alerts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock-chart')
def get_stock_chart():
    """Generate stock level chart data"""
    try:
        inventory_data = inventory_manager.generate_inventory_report()
        
        # Return data for frontend charting
        chart_data = {
            'labels': [item['sku'] for item in inventory_data[:10]],
            'current_stock': [item['current_stock'] for item in inventory_data[:10]],
            'min_stock': [item['min_stock_level'] for item in inventory_data[:10]]
        }
        
        return jsonify(chart_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add-product', methods=['POST'])
def add_product():
    """Add new product"""
    try:
        if not inventory_manager:
            return jsonify({'error': 'Database not initialized', 'success': False}), 500
        
        data = request.json
        success = inventory_manager.add_product(
            sku=data['sku'],
            name=data['name'],
            category=data['category'],
            cost_price=float(data['cost_price']),
            selling_price=float(data['selling_price']),
            initial_stock=int(data.get('initial_stock', 0))
        )
        
        if success:
            return jsonify({'message': 'Product added successfully', 'success': True})
        else:
            return jsonify({'error': 'Failed to add product', 'success': False}), 400
            
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/delete-product', methods=['POST'])
def delete_product():
    """Delete product from inventory"""
    try:
        data = request.json
        sku = data.get('sku')
        
        conn = get_connection()
        cursor = conn.cursor()
        
        param = '%s' if os.environ.get('DATABASE_URL') else '?'
        
        # Get product ID
        cursor.execute(f'SELECT id FROM products WHERE sku = {param}', (sku,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return jsonify({'error': 'Product not found', 'success': False}), 404
        
        product_id = result['id'] if isinstance(result, dict) else result[0]
        
        # Delete related records
        cursor.execute(f'DELETE FROM platform_listings WHERE product_id = {param}', (product_id,))
        cursor.execute(f'DELETE FROM stock_movements WHERE product_id = {param}', (product_id,))
        cursor.execute(f'DELETE FROM orders WHERE product_id = {param}', (product_id,))
        cursor.execute(f'DELETE FROM products WHERE id = {param}', (product_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Product deleted successfully', 'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/update-stock', methods=['POST'])
def update_stock():
    """Update stock levels"""
    try:
        if not inventory_manager:
            return jsonify({'error': 'Database not initialized', 'success': False}), 500
        
        data = request.json
        success = inventory_manager.update_stock(
            sku=data['sku'],
            quantity=int(data['quantity']),
            movement_type=data['movement_type'],
            platform=data.get('platform'),
            order_id=data.get('order_id'),
            notes=data.get('notes')
        )
        
        if success:
            return jsonify({'message': 'Stock updated successfully', 'success': True})
        else:
            return jsonify({'error': 'Failed to update stock', 'success': False}), 400
            
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/export-excel')
def export_excel():
    """Export inventory to Excel"""
    try:
        if not inventory_manager:
            return jsonify({'error': 'Database not initialized'}), 500
        
        # Use the inventory manager's export function
        filepath = inventory_manager.export_to_excel()
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Failed to generate Excel file'}), 500
        
        filename = os.path.basename(filepath)
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/platform-status')
def get_platform_status():
    """Get platform connection status"""
    return jsonify(PLATFORM_CONFIGS)

@app.route('/api/connect-platform', methods=['POST'])
def connect_platform():
    """Connect to platform API"""
    try:
        data = request.json
        platform = data.get('platform')
        credentials = data.get('credentials')
        
        # Store credentials securely (in production, use proper encryption)
        config_file = f'configs/{platform}_config.json'
        os.makedirs('configs', exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(credentials, f)
        
        # Update platform status
        PLATFORM_CONFIGS[platform]['status'] = 'connected'
        
        return jsonify({'message': f'{platform.title()} connected successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sync-platform', methods=['POST'])
def sync_platform():
    """Sync inventory with platform"""
    try:
        data = request.json
        platform = data.get('platform')
        
        # Simulate platform sync
        if PLATFORM_CONFIGS.get(platform, {}).get('status') == 'connected':
            # In production, implement actual API calls
            return jsonify({'message': f'Synced with {platform.title()} successfully'})
        else:
            return jsonify({'error': f'{platform.title()} not connected'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/sales')
def get_sales_report():
    """Generate sales report"""
    try:
        # Get date range from query params
        start_date = request.args.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
        
        # Generate sample sales data
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        sales_data = []
        
        current = start
        while current <= end:
            daily_sales = {
                'date': current.strftime('%Y-%m-%d'),
                'orders': random.randint(5, 50),
                'revenue': round(random.uniform(1000, 10000), 2),
                'profit': round(random.uniform(200, 2000), 2)
            }
            sales_data.append(daily_sales)
            current += timedelta(days=1)
        
        return jsonify(sales_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/inventory-valuation')
def get_inventory_valuation():
    """Get inventory valuation report"""
    try:
        if not inventory_manager:
            return jsonify({'error': 'Database not initialized'}), 500
        
        inventory_data = inventory_manager.generate_inventory_report()
        
        valuation_data = []
        for row in inventory_data:
            valuation_data.append({
                'sku': row['sku'],
                'name': row['name'],
                'category': row['category'],
                'quantity': row['current_stock'],
                'cost_per_unit': row['cost_price'],
                'total_cost': row['current_stock'] * row['cost_price'],
                'selling_price': row['selling_price'],
                'potential_revenue': row['current_stock'] * row['selling_price'],
                'potential_profit': row['current_stock'] * (row['selling_price'] - row['cost_price'])
            })
        
        return jsonify(valuation_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/platform-performance')
def get_platform_performance():
    """Get platform performance report"""
    try:
        # Generate sample platform performance data
        platforms = ['Amazon', 'Flipkart', 'Meesho', 'Shopify', 'eBay']
        performance_data = []
        
        for platform in platforms:
            performance_data.append({
                'platform': platform,
                'orders': random.randint(10, 200),
                'revenue': round(random.uniform(5000, 50000), 2),
                'conversion_rate': round(random.uniform(2, 15), 2),
                'avg_order_value': round(random.uniform(500, 2000), 2),
                'return_rate': round(random.uniform(1, 8), 2)
            })
        
        return jsonify(performance_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['GET', 'POST'])
def handle_orders():
    """Handle order operations"""
    if request.method == 'GET':
        try:
            # Generate sample order data
            orders = []
            platforms = ['Amazon', 'Flipkart', 'Meesho']
            statuses = ['Pending', 'Processing', 'Shipped', 'Delivered']
            
            for i in range(20):
                order = {
                    'order_id': f'ORD{1000 + i}',
                    'platform': random.choice(platforms),
                    'customer_name': f'Customer {i+1}',
                    'product_sku': f'SKU{100 + i}',
                    'quantity': random.randint(1, 5),
                    'amount': round(random.uniform(500, 5000), 2),
                    'status': random.choice(statuses),
                    'order_date': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
                }
                orders.append(order)
            
            return jsonify(orders)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.json
            # Process new order
            order_id = data.get('order_id')
            sku = data.get('sku')
            quantity = int(data.get('quantity'))
            
            # Update stock
            success = inventory_manager.update_stock(
                sku=sku,
                quantity=quantity,
                movement_type='OUT',
                platform=data.get('platform'),
                order_id=order_id,
                notes=f'Order fulfillment for {order_id}'
            )
            
            if success:
                return jsonify({'message': 'Order processed successfully'})
            else:
                return jsonify({'error': 'Failed to process order'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/suppliers', methods=['GET', 'POST'])
def handle_suppliers():
    """Handle supplier operations"""
    if request.method == 'GET':
        try:
            # Generate sample supplier data
            suppliers = [
                {'id': 1, 'name': 'TechSupply Co.', 'contact': 'John Doe', 'email': 'john@techsupply.com', 'phone': '+91-9876543210', 'rating': 4.5},
                {'id': 2, 'name': 'Global Electronics', 'contact': 'Jane Smith', 'email': 'jane@globalelec.com', 'phone': '+91-9876543211', 'rating': 4.2},
                {'id': 3, 'name': 'Accessory World', 'contact': 'Mike Johnson', 'email': 'mike@accworld.com', 'phone': '+91-9876543212', 'rating': 4.8}
            ]
            return jsonify(suppliers)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.json
            # Add new supplier (in production, save to database)
            return jsonify({'message': 'Supplier added successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/charts')
def get_analytics_charts():
    """Get analytics chart data"""
    try:
        # Sales trend chart
        dates = []
        current = datetime.now() - timedelta(days=30)
        end = datetime.now()
        while current <= end:
            dates.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)
        
        sales_trend = {
            'dates': dates,
            'sales': [round(random.uniform(1000, 8000), 2) for _ in dates],
            'orders': [random.randint(5, 50) for _ in dates]
        }
        
        # Category distribution
        categories = ['Electronics', 'Accessories', 'Home & Garden', 'Fashion', 'Sports']
        category_data = {
            'categories': categories,
            'values': [random.randint(50, 500) for _ in categories]
        }
        
        # Platform revenue
        platforms = ['Amazon', 'Flipkart', 'Meesho', 'Shopify', 'eBay']
        platform_revenue = {
            'platforms': platforms,
            'revenue': [round(random.uniform(10000, 100000), 2) for _ in platforms]
        }
        
        return jsonify({
            'sales_trend': sales_trend,
            'category_distribution': category_data,
            'platform_revenue': platform_revenue
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)