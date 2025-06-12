from flask import Flask, jsonify, request
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock database
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "user-service"})

@app.route('/users', methods=['GET'])
def get_users():
    logger.info("Retrieving all users")
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    logger.info(f"Retrieving user with ID: {user_id}")
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json or not 'email' in request.json:
        return jsonify({"error": "Invalid request"}), 400
    
    new_user = {
        "id": users[-1]['id'] + 1 if users else 1,
        "name": request.json['name'],
        "email": request.json['email']
    }
    users.append(new_user)
    logger.info(f"Created new user with ID: {new_user['id']}")
    return jsonify(new_user), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5555))
    app.run(host='0.0.0.0', port=port)
