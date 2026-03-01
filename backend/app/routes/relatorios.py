from flask import Blueprint, jsonify, request

report_routes = Blueprint('report_routes', __name__)


@report_routes.route('/journal', methods=['GET'])
def get_journal():
    # Logic to retrieve journal data
    return jsonify({'message': 'Journal data retrieved'}), 200


@report_routes.route('/trial_balance', methods=['GET'])
def get_trial_balance():
    # Logic to retrieve trial balance data
    return jsonify({'message': 'Trial balance data retrieved'}), 200


@report_routes.route('/balance_sheet', methods=['GET'])
def get_balance_sheet():
    # Logic to retrieve balance sheet data
    return jsonify({'message': 'Balance sheet data retrieved'}), 200


@report_routes.route('/income_statement', methods=['GET'])
def get_income_statement():
    # Logic to retrieve income statement data
    return jsonify({'message': 'Income statement data retrieved'}), 200
