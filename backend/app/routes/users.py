from flask import Blueprint, jsonify, request

# Initialize the Blueprint for user management routes
users_bp = Blueprint('users', __name__)

# Sample data structure to store users
users = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
]

# Endpoint to list all users
@users_bp.route('/users', methods=['GET'])
def list_users():
    return jsonify(users), 200

# Endpoint to get a specific user by ID
@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404

# Endpoint to update a specific user by ID
@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        data = request.get_json()
        user.update(data)
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404

# Endpoint to delete a specific user by ID
@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        users = [u for u in users if u['id'] != user_id]
        return jsonify({'message': 'User deleted successfully'}), 204
    return jsonify({'message': 'User not found'}), 404
