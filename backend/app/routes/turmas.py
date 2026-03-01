from flask import Blueprint, request, jsonify

# Create a Blueprint for the classes management routes
classes_bp = Blueprint('classes', __name__)

# Sample in-memory storage for classes
classes = []

# Route to list all classes
@classes_bp.route('/turmas', methods=['GET'])
def list_classes():
    return jsonify(classes), 200

# Route to create a new class
@classes_bp.route('/turmas', methods=['POST'])
def create_class():
    data = request.get_json()
    # Add input validation as necessary
    new_class = {'id': len(classes) + 1, 'name': data['name']}
    classes.append(new_class)
    return jsonify(new_class), 201

# Route to read a specific class by ID
@classes_bp.route('/turmas/<int:class_id>', methods=['GET'])
def read_class(class_id):
    class_item = next((cls for cls in classes if cls['id'] == class_id), None)
    if class_item:
        return jsonify(class_item), 200
    return jsonify({'error': 'Class not found'}), 404

# Route to update a specific class by ID
@classes_bp.route('/turmas/<int:class_id>', methods=['PUT'])
def update_class(class_id):
    data = request.get_json()
    class_item = next((cls for cls in classes if cls['id'] == class_id), None)
    if class_item:
        class_item['name'] = data['name']
        return jsonify(class_item), 200
    return jsonify({'error': 'Class not found'}), 404

# Route to delete a specific class by ID
@classes_bp.route('/turmas/<int:class_id>', methods=['DELETE'])
def delete_class(class_id):
    global classes
    classes = [cls for cls in classes if cls['id'] != class_id]
    return jsonify({'message': 'Class deleted'}), 204

