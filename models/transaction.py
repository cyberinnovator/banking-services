from database.connection import db
from mysql.connector import Error
from datetime import datetime
import logging

class Transaction:
    def __init__(self, txn_id=None, acc_no=None, type=None, amount=None, date_time=None):
        self.txn_id = txn_id
        self.acc_no = acc_no
        self.type = type
        self.amount = amount
        self.date_time = date_time
    
    @staticmethod
    def create(acc_no, transaction_type, amount):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            
            query = """
            INSERT INTO Transaction (acc_no, type, amount, date_time) 
            VALUES (%s, %s, %s, %s)
            """
            current_time = datetime.now()
            cursor.execute(query, (acc_no, transaction_type, amount, current_time))
            connection.commit()
            
            txn_id = cursor.lastrowid
            cursor.close()
            
            return Transaction(txn_id, acc_no, transaction_type, amount, current_time)
        except Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Error creating transaction: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    @staticmethod
    def get_by_account(acc_no):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT * FROM Transaction 
            WHERE acc_no = %s 
            ORDER BY date_time DESC
            """
            cursor.execute(query, (acc_no,))
            results = cursor.fetchall()
            cursor.close()
            
            return results
        except Error as e:
            logging.error(f"Error fetching transactions: {e}")
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
            SELECT t.*, a.branch_name, c.cust_name 
            FROM Transaction t 
            JOIN Account a ON t.acc_no = a.acc_no 
            JOIN Customer c ON a.cust_id = c.cust_id 
            ORDER BY t.date_time DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            
            return results
        except Error as e:
            logging.error(f"Error fetching all transactions: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    def to_dict(self):
        return {
            'txn_id': self.txn_id,
            'acc_no': self.acc_no,
            'type': self.type,
            'amount': float(self.amount) if self.amount else 0,
            'date_time': self.date_time.isoformat() if self.date_time else None
        }
