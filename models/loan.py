from database.connection import db
from mysql.connector import Error
import logging

class Loan:
    def __init__(self, loan_no=None, branch_name=None, amount=None, status=None, installments_remaining=None):
        self.loan_no = loan_no
        self.branch_name = branch_name
        self.amount = amount
        self.status = status
        self.installments_remaining = installments_remaining
    
    @staticmethod
    def create(branch_name, amount, installments_remaining, cust_id):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            
            # Create loan
            loan_query = """
            INSERT INTO Loan (branch_name, amount, status, installments_remaining) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(loan_query, (branch_name, amount, 'pending', installments_remaining))
            loan_no = cursor.lastrowid
            
            # Create borrower relationship
            borrower_query = "INSERT INTO Borrower (cust_id, loan_no) VALUES (%s, %s)"
            cursor.execute(borrower_query, (cust_id, loan_no))
            
            connection.commit()
            cursor.close()
            
            return Loan(loan_no, branch_name, amount, 'pending', installments_remaining)
        except Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Error creating loan: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    @staticmethod
    def get_by_id(loan_no):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT l.*, c.cust_name, c.cust_id 
            FROM Loan l 
            JOIN Borrower b ON l.loan_no = b.loan_no 
            JOIN Customer c ON b.cust_id = c.cust_id 
            WHERE l.loan_no = %s
            """
            cursor.execute(query, (loan_no,))
            result = cursor.fetchone()
            cursor.close()
            
            return result
        except Error as e:
            logging.error(f"Error fetching loan: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    @staticmethod
    def get_all():
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT l.*, c.cust_name, c.cust_id 
            FROM Loan l 
            JOIN Borrower b ON l.loan_no = b.loan_no 
            JOIN Customer c ON b.cust_id = c.cust_id
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            
            return results
        except Error as e:
            logging.error(f"Error fetching loans: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    def approve(self):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            
            query = "UPDATE Loan SET status = 'approved' WHERE loan_no = %s"
            cursor.execute(query, (self.loan_no,))
            connection.commit()
            cursor.close()
            
            self.status = 'approved'
            return True
        except Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Error approving loan: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    def update_installments(self, remaining):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            
            query = "UPDATE Loan SET installments_remaining = %s WHERE loan_no = %s"
            cursor.execute(query, (remaining, self.loan_no))
            connection.commit()
            cursor.close()
            
            self.installments_remaining = remaining
            return True
        except Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Error updating installments: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
