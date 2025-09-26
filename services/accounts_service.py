from flask import Blueprint, request, jsonify
from models.customer import Customer
from models.account import Account
import logging

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/accounts', methods=['POST'])
def create_account():
    """Add new account with customer details"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['cust_name', 'cust_street', 'cust_city', 'branch_name', 'initial_balance']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create customer first
        customer = Customer.create(
            cust_name=data['cust_name'],
            cust_street=data['cust_street'],
            cust_city=data['cust_city']
        )
        
        # Create account for the customer
        account = Account.create(
            branch_name=data['branch_name'],
            balance=data['initial_balance'],
            cust_id=customer.cust_id
        )
        
        return jsonify({
            'message': 'Account created successfully',
            'account': {
                'acc_no': account.acc_no,
                'branch_name': account.branch_name,
                'balance': float(account.balance),
                'customer': customer.to_dict()
            }
        }), 201
        
    except Exception as e:
        logging.error(f"Error creating account: {e}")
        return jsonify({'error': 'Failed to create account'}), 500

@accounts_bp.route('/accounts/<int:acc_no>', methods=['GET'])
def get_account(acc_no):
    """Get account details by account number"""
    try:
        account = Account.get_by_id(acc_no)
        
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        return jsonify({
            'account': {
                'acc_no': account['acc_no'],
                'branch_name': account['branch_name'],
                'balance': float(account['balance']),
                'customer': {
                    'cust_id': account['cust_id'],
                    'cust_name': account['cust_name'],
                    'cust_street': account['cust_street'],
                    'cust_city': account['cust_city']
                }
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Error fetching account: {e}")
        return jsonify({'error': 'Failed to fetch account'}), 500

@accounts_bp.route('/accounts/<int:acc_no>', methods=['PUT'])
def update_account(acc_no):
    """Edit account details"""
    try:
        data = request.get_json()
        
        # Get existing account
        account_data = Account.get_by_id(acc_no)
        if not account_data:
            return jsonify({'error': 'Account not found'}), 404
        
        # Update account details
        account = Account(
            acc_no=acc_no,
            branch_name=data.get('branch_name', account_data['branch_name']),
            balance=data.get('balance', account_data['balance']),
            cust_id=account_data['cust_id']
        )
        account.update()
        
        # Update customer details if provided
        if any(field in data for field in ['cust_name', 'cust_street', 'cust_city']):
            customer = Customer.get_by_id(account_data['cust_id'])
            if customer:
                customer.cust_name = data.get('cust_name', customer.cust_name)
                customer.cust_street = data.get('cust_street', customer.cust_street)
                customer.cust_city = data.get('cust_city', customer.cust_city)
                customer.update()
        
        # Get updated account data
        updated_account = Account.get_by_id(acc_no)
        
        return jsonify({
            'message': 'Account updated successfully',
            'account': {
                'acc_no': updated_account['acc_no'],
                'branch_name': updated_account['branch_name'],
                'balance': float(updated_account['balance']),
                'customer': {
                    'cust_id': updated_account['cust_id'],
                    'cust_name': updated_account['cust_name'],
                    'cust_street': updated_account['cust_street'],
                    'cust_city': updated_account['cust_city']
                }
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Error updating account: {e}")
        return jsonify({'error': 'Failed to update account'}), 500

@accounts_bp.route('/accounts/<int:acc_no>', methods=['DELETE'])
def delete_account(acc_no):
    """Delete account"""
    try:
        # Check if account exists
        account_data = Account.get_by_id(acc_no)
        if not account_data:
            return jsonify({'error': 'Account not found'}), 404
        
        # Delete account
        account = Account(acc_no=acc_no)
        account.delete()
        
        return jsonify({'message': 'Account deleted successfully'}), 200
        
    except Exception as e:
        logging.error(f"Error deleting account: {e}")
        return jsonify({'error': 'Failed to delete account'}), 500

@accounts_bp.route('/accounts', methods=['GET'])
def list_accounts():
    """List all accounts"""
    try:
        accounts = Account.get_all()
        
        account_list = []
        for account in accounts:
            account_list.append({
                'acc_no': account['acc_no'],
                'branch_name': account['branch_name'],
                'balance': float(account['balance']),
                'customer': {
                    'cust_id': account['cust_id'],
                    'cust_name': account['cust_name'],
                    'cust_street': account['cust_street'],
                    'cust_city': account['cust_city']
                }
            })
        
        return jsonify({
            'accounts': account_list,
            'total': len(account_list)
        }), 200
        
    except Exception as e:
        logging.error(f"Error listing accounts: {e}")
        return jsonify({'error': 'Failed to list accounts'}), 500

# Additional endpoint for customer management
@accounts_bp.route('/customers', methods=['GET'])
def list_customers():
    """List all customers"""
    try:
        customers = Customer.get_all()
        
        customer_list = [customer.to_dict() for customer in customers]
        
        return jsonify({
            'customers': customer_list,
            'total': len(customer_list)
        }), 200
        
    except Exception as e:
        logging.error(f"Error listing customers: {e}")
        return jsonify({'error': 'Failed to list customers'}), 500

@accounts_bp.route('/customers/<int:cust_id>', methods=['GET'])
def get_customer(cust_id):
    """Get customer details"""
    try:
        customer = Customer.get_by_id(cust_id)
        
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        return jsonify({'customer': customer.to_dict()}), 200
        
    except Exception as e:
        logging.error(f"Error fetching customer: {e}")
        return jsonify({'error': 'Failed to fetch customer'}), 500
