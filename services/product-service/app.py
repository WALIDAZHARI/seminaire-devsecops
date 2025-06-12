from flask import Flask, jsonify, request
import os
import logging
import requests

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock database
products = [
    {"id": 1, "name": "Laptop", "price": 999.99, "in_stock": True},
    {"id": 2, "name": "Smartphone", "price": 499.99, "in_stock": True},
    {"id": 3, "name": "Headphones", "price": 99.99, "in_stock": False}
]

# Configuration
USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL', 'http://user-service:5000')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "product-service"})

@app.route('/products', methods=['GET'])
def get_products():
    logger.info("Retrieving all products")
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    logger.info(f"Retrieving product with ID: {product_id}")
    product = next((product for product in products if product['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/products', methods=['POST'])
def create_product():
    if not request.json or not 'name' in request.json or not 'price' in request.json:
        return jsonify({"error": "Invalid request"}), 400
    
    new_product = {
        "id": products[-1]['id'] + 1 if products else 1,
        "name": request.json['name'],
        "price": request.json['price'],
        "in_stock": request.json.get('in_stock', True)
    }
    products.append(new_product)
    logger.info(f"Created new product with ID: {new_product['id']}")
    return jsonify(new_product), 201

@app.route('/products/user/<int:user_id>', methods=['GET'])
def get_user_products(user_id):
    """Get products with user information (demonstrates service-to-service communication)"""
    try:
        # Call user service to get user details
        response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
        if response.status_code == 200:
            user = response.json()
            # For demo purposes, just return some products with user info
            return jsonify({
                "user": user,
                "recommended_products": products[:2]
            })
        return jsonify({"error": "User not found"}), 404
    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with user service: {str(e)}")
        return jsonify({"error": "Service communication error"}), 503

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5556))
    app.run(host='0.0.0.0', port=port)
