from database.connection import db
from mysql.connector import Error
import logging

class Account:
    def __init__(self, acc_no=None, branch_name=None, balance=None, cust_id=None):
        self.acc_no = acc_no
        self.branch_name = branch_name
        self.balance = balance
        self.cust_id = cust_id
    
    @staticmethod
    def create(branch_name, balance, cust_id):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            
            query = """
            INSERT INTO Account (branch_name, balance, cust_id) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (branch_name, balance, cust_id))
            
            acc_no = cursor.lastrowid
            cursor.close()
            
            return Account(acc_no, branch_name, balance, cust_id)
        except Error as e:
            logging.error(f"Error creating account: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    @staticmethod
    def get_by_id(acc_no):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT a.*, c.cust_name, c.cust_street, c.cust_city 
            FROM Account a 
            JOIN Customer c ON a.cust_id = c.cust_id 
            WHERE a.acc_no = %s
            """
            cursor.execute(query, (acc_no,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return result
            return None
        except Error as e:
            logging.error(f"Error fetching account: {e}")
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
            SELECT a.*, c.cust_name, c.cust_street, c.cust_city 
            FROM Account a 
            JOIN Customer c ON a.cust_id = c.cust_id
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            
            return results
        except Error as e:
            logging.error(f"Error fetching accounts: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    def update(self):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            
            query = """
            UPDATE Account 
            SET branch_name = %s, balance = %s 
            WHERE acc_no = %s
            """
            cursor.execute(query, (self.branch_name, self.balance, self.acc_no))
            cursor.close()
            
            return True
        except Error as e:
            logging.error(f"Error updating account: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    def delete(self):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            
            query = "DELETE FROM Account WHERE acc_no = %s"
            cursor.execute(query, (self.acc_no,))
            cursor.close()
            
            return True
        except Error as e:
            logging.error(f"Error deleting account: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    def update_balance(self, new_balance):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            
            query = "UPDATE Account SET balance = %s WHERE acc_no = %s"
            cursor.execute(query, (new_balance, self.acc_no))
            cursor.close()
            
            self.balance = new_balance
            return True
        except Error as e:
            logging.error(f"Error updating balance: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
