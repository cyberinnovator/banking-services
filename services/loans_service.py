from flask import Blueprint, request, jsonify
from models.loan import Loan
from models.customer import Customer
import logging

loans_bp = Blueprint('loans', __name__)

@loans_bp.route('/loans', methods=['POST'])
def apply_for_loan():
    """Apply for a new loan"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['cust_id', 'branch_name', 'amount', 'installments']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate customer exists
        customer = Customer.get_by_id(data['cust_id'])
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        # Validate amount and installments
        if data['amount'] <= 0:
            return jsonify({'error': 'Loan amount must be positive'}), 400
        
        if data['installments'] <= 0:
            return jsonify({'error': 'Installments must be positive'}), 400
        
        # Create loan
        loan = Loan.create(
            branch_name=data['branch_name'],
            amount=data['amount'],
            installments_remaining=data['installments'],
            cust_id=data['cust_id']
        )
        
        return jsonify({
            'message': 'Loan application submitted successfully',
            'loan': {
                'loan_no': loan.loan_no,
                'branch_name': loan.branch_name,
                'amount': float(loan.amount),
                'status': loan.status,
                'installments_remaining': loan.installments_remaining,
                'customer': customer.to_dict()
            }
        }), 201
        
    except Exception as e:
        logging.error(f"Error applying for loan: {e}")
        return jsonify({'error': 'Failed to apply for loan'}), 500

@loans_bp.route('/loans/<int:loan_no>', methods=['GET'])
def get_loan(loan_no):
    """Get loan details by loan number"""
    try:
        loan = Loan.get_by_id(loan_no)
        
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404
        
        return jsonify({
            'loan': {
                'loan_no': loan['loan_no'],
                'branch_name': loan['branch_name'],
                'amount': float(loan['amount']),
                'status': loan['status'],
                'installments_remaining': loan['installments_remaining'],
                'customer': {
                    'cust_id': loan['cust_id'],
                    'cust_name': loan['cust_name']
                }
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Error fetching loan: {e}")
        return jsonify({'error': 'Failed to fetch loan'}), 500

@loans_bp.route('/loans/<int:loan_no>/approve', methods=['PUT'])
def approve_loan(loan_no):
    """Approve a loan"""
    try:
        # Check if loan exists
        loan_data = Loan.get_by_id(loan_no)
        if not loan_data:
            return jsonify({'error': 'Loan not found'}), 404
        
        # Check if loan is already approved
        if loan_data['status'] == 'approved':
            return jsonify({'error': 'Loan is already approved'}), 400
        
        # Approve the loan
        loan = Loan(
            loan_no=loan_no,
            status=loan_data['status']
        )
        loan.approve()
        
        # Get updated loan data
        updated_loan = Loan.get_by_id(loan_no)
        
        return jsonify({
            'message': 'Loan approved successfully',
            'loan': {
                'loan_no': updated_loan['loan_no'],
                'branch_name': updated_loan['branch_name'],
                'amount': float(updated_loan['amount']),
                'status': updated_loan['status'],
                'installments_remaining': updated_loan['installments_remaining'],
                'customer': {
                    'cust_id': updated_loan['cust_id'],
                    'cust_name': updated_loan['cust_name']
                }
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Error approving loan: {e}")
        return jsonify({'error': 'Failed to approve loan'}), 500

@loans_bp.route('/loans/<int:loan_no>/installments', methods=['GET'])
def get_remaining_installments(loan_no):
    """Get remaining installments for a loan"""
    try:
        loan = Loan.get_by_id(loan_no)
        
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404
        
        return jsonify({
            'loan_no': loan['loan_no'],
            'installments_remaining': loan['installments_remaining'],
            'amount': float(loan['amount']),
            'status': loan['status'],
            'customer': {
                'cust_id': loan['cust_id'],
                'cust_name': loan['cust_name']
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Error fetching installments: {e}")
        return jsonify({'error': 'Failed to fetch installments'}), 500

@loans_bp.route('/loans/<int:loan_no>/installments', methods=['PUT'])
def update_installments(loan_no):
    """Update remaining installments (for payment processing)"""
    try:
        data = request.get_json()
        
        if 'installments_remaining' not in data:
            return jsonify({'error': 'Missing installments_remaining field'}), 400
        
        # Check if loan exists
        loan_data = Loan.get_by_id(loan_no)
        if not loan_data:
            return jsonify({'error': 'Loan not found'}), 404
        
        # Validate installments
        new_installments = data['installments_remaining']
        if new_installments < 0:
            return jsonify({'error': 'Installments remaining cannot be negative'}), 400
        
        # Update installments
        loan = Loan(
            loan_no=loan_no,
            installments_remaining=loan_data['installments_remaining']
        )
        loan.update_installments(new_installments)
        
        # Get updated loan data
        updated_loan = Loan.get_by_id(loan_no)
        
        return jsonify({
            'message': 'Installments updated successfully',
            'loan': {
                'loan_no': updated_loan['loan_no'],
                'installments_remaining': updated_loan['installments_remaining'],
                'amount': float(updated_loan['amount']),
                'status': updated_loan['status']
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Error updating installments: {e}")
        return jsonify({'error': 'Failed to update installments'}), 500

@loans_bp.route('/loans', methods=['GET'])
def list_loans():
    """List all loans"""
    try:
        loans = Loan.get_all()
        
        loan_list = []
        for loan in loans:
            loan_list.append({
                'loan_no': loan['loan_no'],
                'branch_name': loan['branch_name'],
                'amount': float(loan['amount']),
                'status': loan['status'],
                'installments_remaining': loan['installments_remaining'],
                'customer': {
                    'cust_id': loan['cust_id'],
                    'cust_name': loan['cust_name']
                }
            })
        
        return jsonify({
            'loans': loan_list,
            'total': len(loan_list)
        }), 200
        
    except Exception as e:
        logging.error(f"Error listing loans: {e}")
        return jsonify({'error': 'Failed to list loans'}), 500

@loans_bp.route('/loans/status/<status>', methods=['GET'])
def get_loans_by_status(status):
    """Get loans by status (pending, approved, rejected)"""
    try:
        if status not in ['pending', 'approved', 'rejected']:
            return jsonify({'error': 'Invalid status. Use: pending, approved, or rejected'}), 400
        
        loans = Loan.get_all()
        filtered_loans = [loan for loan in loans if loan['status'] == status]
        
        loan_list = []
        for loan in filtered_loans:
            loan_list.append({
                'loan_no': loan['loan_no'],
                'branch_name': loan['branch_name'],
                'amount': float(loan['amount']),
                'status': loan['status'],
                'installments_remaining': loan['installments_remaining'],
                'customer': {
                    'cust_id': loan['cust_id'],
                    'cust_name': loan['cust_name']
                }
            })
        
        return jsonify({
            'loans': loan_list,
            'total': len(loan_list),
            'status': status
        }), 200
        
    except Exception as e:
        logging.error(f"Error fetching loans by status: {e}")
        return jsonify({'error': 'Failed to fetch loans by status'}), 500
