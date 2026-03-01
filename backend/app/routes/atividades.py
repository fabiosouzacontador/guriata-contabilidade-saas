from flask import Blueprint, request, jsonify
from your_project_name.models import Activity  # Adjust this import according to your project structure

activities_bp = Blueprint('activities', __name__)

# Create an Activity
@activities_bp.route('/activities', methods=['POST'])
def create_activity():
    data = request.get_json()
    new_activity = Activity(**data)  # Ensure the dictionary keys match your model columns
    new_activity.save()  # Implement save method in your model class
    return jsonify(new_activity.to_dict()), 201

# Read all Activities
@activities_bp.route('/activities', methods=['GET'])
def get_activities():
    activities = Activity.query.all()  # Retrieve all activities
    return jsonify([activity.to_dict() for activity in activities]), 200

# Read a single Activity
@activities_bp.route('/activities/<int:id>', methods=['GET'])
def get_activity(id):
    activity = Activity.query.get(id)  # Retrieve activity by ID
    if activity is not None:
        return jsonify(activity.to_dict()), 200
    return jsonify({'message': 'Activity not found'}), 404

# Update an Activity
@activities_bp.route('/activities/<int:id>', methods=['PUT'])
def update_activity(id):
    data = request.get_json()
    activity = Activity.query.get(id)
    if activity is not None:
        for key, value in data.items():
            setattr(activity, key, value)
        activity.save()  # Implement save method in your model class
        return jsonify(activity.to_dict()), 200
    return jsonify({'message': 'Activity not found'}), 404

# Delete an Activity
@activities_bp.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get(id)
    if activity is not None:
        activity.delete()  # Implement delete method in your model class
        return jsonify({'message': 'Activity deleted successfully'}), 200
    return jsonify({'message': 'Activity not found'}), 404

# Remember to register this blueprint in your main app file.
# app.register_blueprint(activities_bp)