from flask import Blueprint, request, jsonify
from models.transaction import Transaction
from models.account import Account
from decimal import Decimal
import logging

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions/deposit', methods=['POST'])
def deposit_money():
    """Deposit money to an account"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['acc_no', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        acc_no = data['acc_no']
        amount = Decimal(str(data['amount']))
        
        # Validate amount
        if amount <= 0:
            return jsonify({'error': 'Deposit amount must be positive'}), 400
        
        # Check if account exists
        account_data = Account.get_by_id(acc_no)
        if not account_data:
            return jsonify({'error': 'Account not found'}), 404
        
        # Calculate new balance
        current_balance = Decimal(str(account_data['balance']))
        new_balance = current_balance + amount
        
        # Update account balance
        account = Account(
            acc_no=acc_no,
            branch_name=account_data['branch_name'],
            balance=new_balance,
            cust_id=account_data['cust_id']
        )
        account.update_balance(float(new_balance))
        
        # Create transaction record
        transaction = Transaction.create(acc_no, 'deposit', float(amount))
        
        return jsonify({
            'message': 'Deposit successful',
            'transaction': transaction.to_dict(),
            'account': {
                'acc_no': acc_no,
                'previous_balance': float(current_balance),
                'new_balance': float(new_balance),
                'deposited_amount': float(amount)
            }
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid amount format'}), 400
    except Exception as e:
        logging.error(f"Error processing deposit: {e}")
        return jsonify({'error': 'Failed to process deposit'}), 500

@transactions_bp.route('/transactions/withdraw', methods=['POST'])
def withdraw_money():
    """Withdraw money from an account"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['acc_no', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        acc_no = data['acc_no']
        amount = Decimal(str(data['amount']))
        
        # Validate amount
        if amount <= 0:
            return jsonify({'error': 'Withdrawal amount must be positive'}), 400
        
        # Check if account exists
        account_data = Account.get_by_id(acc_no)
        if not account_data:
            return jsonify({'error': 'Account not found'}), 404
        
        # Check sufficient balance
        current_balance = Decimal(str(account_data['balance']))
        if current_balance < amount:
            return jsonify({
                'error': 'Insufficient balance',
                'current_balance': float(current_balance),
                'requested_amount': float(amount)
            }), 400
        
        # Calculate new balance
        new_balance = current_balance - amount
        
        # Update account balance
        account = Account(
            acc_no=acc_no,
            branch_name=account_data['branch_name'],
            balance=new_balance,
            cust_id=account_data['cust_id']
        )
        account.update_balance(float(new_balance))
        
        # Create transaction record
        transaction = Transaction.create(acc_no, 'withdrawal', float(amount))
        
        return jsonify({
            'message': 'Withdrawal successful',
            'transaction': transaction.to_dict(),
            'account': {
                'acc_no': acc_no,
                'previous_balance': float(current_balance),
                'new_balance': float(new_balance),
                'withdrawn_amount': float(amount)
            }
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid amount format'}), 400
    except Exception as e:
        logging.error(f"Error processing withdrawal: {e}")
        return jsonify({'error': 'Failed to process withdrawal'}), 500

@transactions_bp.route('/transactions/<int:acc_no>', methods=['GET'])
def get_transaction_history(acc_no):
    """Get transaction history for a specific account"""
    try:
        # Check if account exists
        account_data = Account.get_by_id(acc_no)
        if not account_data:
            return jsonify({'error': 'Account not found'}), 404
        
        # Get transaction history
        transactions = Transaction.get_by_account(acc_no)
        
        # Format transactions
        transaction_list = []
        for txn in transactions:
            transaction_list.append({
                'txn_id': txn['txn_id'],
                'type': txn['type'],
                'amount': float(txn['amount']),
                'date_time': txn['date_time'].isoformat() if txn['date_time'] else None
            })
        
        return jsonify({
            'account': {
                'acc_no': acc_no,
                'branch_name': account_data['branch_name'],
                'current_balance': float(account_data['balance']),
                'customer': {
                    'cust_id': account_data['cust_id'],
                    'cust_name': account_data['cust_name']
                }
            },
            'transactions': transaction_list,
            'total_transactions': len(transaction_list)
        }), 200
        
    except Exception as e:
        logging.error(f"Error fetching transaction history: {e}")
        return jsonify({'error': 'Failed to fetch transaction history'}), 500

@transactions_bp.route('/transactions', methods=['GET'])
def get_all_transactions():
    """Get all transactions across all accounts"""
    try:
        transactions = Transaction.get_all()
        
        # Format transactions
        transaction_list = []
        for txn in transactions:
            transaction_list.append({
                'txn_id': txn['txn_id'],
                'acc_no': txn['acc_no'],
                'type': txn['type'],
                'amount': float(txn['amount']),
                'date_time': txn['date_time'].isoformat() if txn['date_time'] else None,
                'account_info': {
                    'branch_name': txn['branch_name'],
                    'customer_name': txn['cust_name']
                }
            })
        
        return jsonify({
            'transactions': transaction_list,
            'total_transactions': len(transaction_list)
        }), 200
        
    except Exception as e:
        logging.error(f"Error fetching all transactions: {e}")
        return jsonify({'error': 'Failed to fetch transactions'}), 500

@transactions_bp.route('/transactions/summary/<int:acc_no>', methods=['GET'])
def get_account_summary(acc_no):
    """Get account summary with transaction statistics"""
    try:
        # Check if account exists
        account_data = Account.get_by_id(acc_no)
        if not account_data:
            return jsonify({'error': 'Account not found'}), 404
        
        # Get transaction history
        transactions = Transaction.get_by_account(acc_no)
        
        # Calculate summary statistics
        total_deposits = sum(float(txn['amount']) for txn in transactions if txn['type'] == 'deposit')
        total_withdrawals = sum(float(txn['amount']) for txn in transactions if txn['type'] == 'withdrawal')
        deposit_count = len([txn for txn in transactions if txn['type'] == 'deposit'])
        withdrawal_count = len([txn for txn in transactions if txn['type'] == 'withdrawal'])
        
        return jsonify({
            'account': {
                'acc_no': acc_no,
                'branch_name': account_data['branch_name'],
                'current_balance': float(account_data['balance']),
                'customer': {
                    'cust_id': account_data['cust_id'],
                    'cust_name': account_data['cust_name']
                }
            },
            'summary': {
                'total_deposits': total_deposits,
                'total_withdrawals': total_withdrawals,
                'deposit_count': deposit_count,
                'withdrawal_count': withdrawal_count,
                'total_transactions': len(transactions),
                'net_change': total_deposits - total_withdrawals
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Error generating account summary: {e}")
        return jsonify({'error': 'Failed to generate account summary'}), 500

@transactions_bp.route('/transactions/transfer', methods=['POST'])
def transfer_money():
    """Transfer money between accounts"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['from_acc_no', 'to_acc_no', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        from_acc_no = data['from_acc_no']
        to_acc_no = data['to_acc_no']
        amount = Decimal(str(data['amount']))
        
        # Validate amount
        if amount <= 0:
            return jsonify({'error': 'Transfer amount must be positive'}), 400
        
        # Check if accounts are different
        if from_acc_no == to_acc_no:
            return jsonify({'error': 'Cannot transfer to the same account'}), 400
        
        # Check if both accounts exist
        from_account_data = Account.get_by_id(from_acc_no)
        to_account_data = Account.get_by_id(to_acc_no)
        
        if not from_account_data:
            return jsonify({'error': 'Source account not found'}), 404
        
        if not to_account_data:
            return jsonify({'error': 'Destination account not found'}), 404
        
        # Check sufficient balance in source account
        from_balance = Decimal(str(from_account_data['balance']))
        if from_balance < amount:
            return jsonify({
                'error': 'Insufficient balance in source account',
                'current_balance': float(from_balance),
                'requested_amount': float(amount)
            }), 400
        
        # Calculate new balances
        new_from_balance = from_balance - amount
        to_balance = Decimal(str(to_account_data['balance']))
        new_to_balance = to_balance + amount
        
        # Update both account balances
        from_account = Account(
            acc_no=from_acc_no,
            branch_name=from_account_data['branch_name'],
            balance=new_from_balance,
            cust_id=from_account_data['cust_id']
        )
        from_account.update_balance(float(new_from_balance))
        
        to_account = Account(
            acc_no=to_acc_no,
            branch_name=to_account_data['branch_name'],
            balance=new_to_balance,
            cust_id=to_account_data['cust_id']
        )
        to_account.update_balance(float(new_to_balance))
        
        # Create transaction records
        withdrawal_txn = Transaction.create(from_acc_no, 'transfer_out', float(amount))
        deposit_txn = Transaction.create(to_acc_no, 'transfer_in', float(amount))
        
        return jsonify({
            'message': 'Transfer successful',
            'transfer_details': {
                'from_account': {
                    'acc_no': from_acc_no,
                    'previous_balance': float(from_balance),
                    'new_balance': float(new_from_balance)
                },
                'to_account': {
                    'acc_no': to_acc_no,
                    'previous_balance': float(to_balance),
                    'new_balance': float(new_to_balance)
                },
                'amount': float(amount)
            },
            'transactions': [
                withdrawal_txn.to_dict(),
                deposit_txn.to_dict()
            ]
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid amount format'}), 400
    except Exception as e:
        logging.error(f"Error processing transfer: {e}")
        return jsonify({'error': 'Failed to process transfer'}), 500
