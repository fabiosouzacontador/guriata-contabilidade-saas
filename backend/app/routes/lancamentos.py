from flask import Blueprint, request, jsonify

# define the blueprint
lancamentos_bp = Blueprint('lancamentos', __name__)

# Sample in-memory data structure for accounting entries
entries = []

# POST endpoint to create a new accounting entry
@lancamentos_bp.route('/lancamentos', methods=['POST'])
def create_entry():
    data = request.get_json()
    entry = {
        'id': len(entries) + 1,
        'description': data['description'],
        'amount': data['amount'],
        'date': data['date']
    }
    entries.append(entry)
    return jsonify(entry), 201

# GET endpoint to retrieve all accounting entries
@lancamentos_bp.route('/lancamentos', methods=['GET'])
def get_entries():
    return jsonify(entries)

# PUT endpoint to update an accounting entry by ID
@lancamentos_bp.route('/lancamentos/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    data = request.get_json()
    entry = next((entry for entry in entries if entry['id'] == entry_id), None)
    if entry:
        entry['description'] = data.get('description', entry['description'])
        entry['amount'] = data.get('amount', entry['amount'])
        entry['date'] = data.get('date', entry['date'])
        return jsonify(entry)
    else:
        return jsonify({'error': 'Entry not found'}), 404

# DELETE endpoint to delete an accounting entry by ID
@lancamentos_bp.route('/lancamentos/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    global entries
    entries = [entry for entry in entries if entry['id'] != entry_id]
    return jsonify({'result': 'Entry deleted'}), 200

# Endpoint to get reports
@lancamentos_bp.route('/reports/saldo', methods=['GET'])
def report_saldo():
    saldo = sum(entry['amount'] for entry in entries)
    return jsonify({'saldo': saldo})

@lancamentos_bp.route('/reports/diario', methods=['GET'])
def report_diario():
    return jsonify(entries)

@lancamentos_bp.route('/reports/balancete', methods=['GET'])
def report_balancete():
    # This is a placeholder for more complex logic
    balancete = {
        'entries_count': len(entries),
        'total_amount': sum(entry['amount'] for entry in entries)
    }
    return jsonify(balancete)

