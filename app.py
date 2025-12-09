"""
MoonHub Inventory Management System
Simple Flask Web Application
"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from inventory_manager import InventoryManager
import os

app = Flask(__name__)
app.secret_key = 'moonhub_secret_key'
CORS(app)

# Initialize inventory manager
inventory = InventoryManager()

@app.route('/')
def index():
    """Home page"""
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/dashboard-stats')
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        products = inventory.get_all_products()
        low_stock = inventory.get_low_stock_alerts()
        
        total_products = len(products)
        total_value = sum(p['current_stock'] * p['cost_price'] for p in products)
        low_stock_count = len(low_stock)
        out_of_stock = sum(1 for p in products if p['current_stock'] == 0)
        
        # Calculate average profit margin
        margins = []
        for p in products:
            if p['selling_price'] > 0:
                margin = ((p['selling_price'] - p['cost_price']) / p['selling_price']) * 100
                margins.append(margin)
        
        avg_margin = sum(margins) / len(margins) if margins else 0
        
        return jsonify({
            'total_products': total_products,
            'total_stock_value': round(total_value, 2),
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock,
            'avg_profit_margin': round(avg_margin, 1)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inventory-data')
def get_inventory_data():
    """Get all inventory data"""
    try:
        products = inventory.get_all_products()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add-product', methods=['POST'])
def add_product():
    """Add new product"""
    try:
        data = request.json
        success = inventory.add_product(
            sku=data['sku'],
            name=data['name'],
            category=data['category'],
            cost_price=float(data['cost_price']),
            selling_price=float(data['selling_price']),
            initial_stock=int(data.get('initial_stock', 0))
        )
        
        if success:
            return jsonify({'success': True, 'message': 'Product added successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to add product'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/update-stock', methods=['POST'])
def update_stock():
    """Update stock levels"""
    try:
        data = request.json
        success = inventory.update_stock(
            sku=data['sku'],
            quantity=int(data['quantity']),
            movement_type=data['movement_type'],
            notes=data.get('notes')
        )
        
        if success:
            return jsonify({'success': True, 'message': 'Stock updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update stock'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/delete-product', methods=['POST'])
def delete_product():
    """Delete product"""
    try:
        data = request.json
        success = inventory.delete_product(data['sku'])
        
        if success:
            return jsonify({'success': True, 'message': 'Product deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export-excel')
def export_excel():
    """Export inventory to Excel"""
    try:
        filepath = inventory.export_to_excel()
        if filepath and os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, download_name=os.path.basename(filepath))
        else:
            return jsonify({'error': 'Failed to generate Excel file'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add sample data on startup
def add_sample_data():
    """Add sample products if database is empty"""
    try:
        products = inventory.get_all_products()
        if len(products) == 0:
            sample_products = [
                ("WH001", "Wireless Headphones", "Electronics", 800, 1500, 45),
                ("KB002", "Mechanical Keyboard", "Electronics", 1200, 2200, 23),
                ("MS003", "Gaming Mouse", "Electronics", 600, 1100, 67),
                ("CH004", "Phone Charger", "Accessories", 150, 350, 120),
                ("CS005", "Phone Case", "Accessories", 100, 250, 8),
                ("SP006", "Bluetooth Speaker", "Electronics", 900, 1800, 0),
                ("CB007", "USB Cable", "Accessories", 50, 150, 200),
                ("TB008", "Tablet Stand", "Accessories", 300, 650, 35)
            ]
            
            for sku, name, category, cost, selling, stock in sample_products:
                inventory.add_product(sku, name, category, cost, selling, stock)
            
            print(f"✅ Added {len(sample_products)} sample products")
    except Exception as e:
        print(f"Warning: Could not add sample data: {e}")

if __name__ == '__main__':
    print("🌙 Starting MoonHub Inventory System...")
    add_sample_data()
    print("🚀 Server starting at http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)