from flask import Blueprint, jsonify, request

# Create a blueprint for the schools management routes
escolas_bp = Blueprint('escolas', __name__)

# In-memory storage for demonstration purposes
schools = []

# List all schools
@escolas_bp.route('/', methods=['GET'])
def list_schools():
    return jsonify(schools), 200

# Create a new school
@escolas_bp.route('/', methods=['POST'])
def create_school():
    data = request.json
    new_school = {
        'id': len(schools) + 1,
        'name': data.get('name'),
        'location': data.get('location'),
        'students_count': data.get('students_count')
    }
    schools.append(new_school)
    return jsonify(new_school), 201

# Read a specific school
@escolas_bp.route('/<int:school_id>', methods=['GET'])
def read_school(school_id):
    school = next((s for s in schools if s['id'] == school_id), None)
    if school:
        return jsonify(school), 200
    return jsonify({'error': 'School not found'}), 404

# Update a specific school
@escolas_bp.route('/<int:school_id>', methods=['PUT'])
def update_school(school_id):
    data = request.json
    school = next((s for s in schools if s['id'] == school_id), None)
    if school:
        school['name'] = data.get('name', school['name'])
        school['location'] = data.get('location', school['location'])
        school['students_count'] = data.get('students_count', school['students_count'])
        return jsonify(school), 200
    return jsonify({'error': 'School not found'}), 404

# Delete a specific school
@escolas_bp.route('/<int:school_id>', methods=['DELETE'])
def delete_school(school_id):
    global schools
    schools = [s for s in schools if s['id'] != school_id]
    return jsonify({'message': 'School deleted'}), 204
