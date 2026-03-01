from flask import Blueprint, request, jsonify

contas = Blueprint('contas', __name__)

# In-memory database emulation for demonstration
accounts_db = {}
next_id = 1

# List accounts
@contas.route('/accounts', methods=['GET'])
def list_accounts():
    return jsonify(accounts_db), 200

# Create account
@contas.route('/accounts', methods=['POST'])
def create_account():
    global next_id
    data = request.json
    account = {
        'id': next_id,
        'name': data['name'],
        'balance': data['balance'],
    }
    accounts_db[next_id] = account
    next_id += 1
    return jsonify(account), 201

# Read account
@contas.route('/accounts/<int:account_id>', methods=['GET'])
def read_account(account_id):
    account = accounts_db.get(account_id)
    if account:
        return jsonify(account), 200
    return jsonify({'error': 'Account not found'}), 404

# Update account
@contas.route('/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    data = request.json
    account = accounts_db.get(account_id)
    if account:
        account['name'] = data.get('name', account['name'])
        account['balance'] = data.get('balance', account['balance'])
        return jsonify(account), 200
    return jsonify({'error': 'Account not found'}), 404

# Delete account
@contas.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account = accounts_db.pop(account_id, None)
    if account:
        return jsonify({'message': 'Account deleted'}), 200
    return jsonify({'error': 'Account not found'}), 404
