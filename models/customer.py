from database.connection import db
from mysql.connector import Error
import logging

class Customer:
    def __init__(self, cust_id=None, cust_name=None, cust_street=None, cust_city=None):
        self.cust_id = cust_id
        self.cust_name = cust_name
        self.cust_street = cust_street
        self.cust_city = cust_city
    
    @staticmethod
    def create(cust_name, cust_street, cust_city):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            
            query = """
            INSERT INTO Customer (cust_name, cust_street, cust_city) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (cust_name, cust_street, cust_city))
            connection.commit()
            
            cust_id = cursor.lastrowid
            cursor.close()
            
            return Customer(cust_id, cust_name, cust_street, cust_city)
        except Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Error creating customer: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    @staticmethod
    def get_by_id(cust_id):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM Customer WHERE cust_id = %s"
            cursor.execute(query, (cust_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return Customer(**result)
            return None
        except Error as e:
            logging.error(f"Error fetching customer: {e}")
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
            
            query = "SELECT * FROM Customer"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            
            return [Customer(**row) for row in results]
        except Error as e:
            logging.error(f"Error fetching customers: {e}")
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
            UPDATE Customer 
            SET cust_name = %s, cust_street = %s, cust_city = %s 
            WHERE cust_id = %s
            """
            cursor.execute(query, (self.cust_name, self.cust_street, self.cust_city, self.cust_id))
            connection.commit()
            cursor.close()
            
            return True
        except Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Error updating customer: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    def delete(self):
        connection = None
        try:
            connection = db.get_connection()
            cursor = connection.cursor()
            
            query = "DELETE FROM Customer WHERE cust_id = %s"
            cursor.execute(query, (self.cust_id,))
            connection.commit()
            cursor.close()
            
            return True
        except Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Error deleting customer: {e}")
            raise e
        finally:
            if connection:
                db.return_connection(connection)
    
    def to_dict(self):
        return {
            'cust_id': self.cust_id,
            'cust_name': self.cust_name,
            'cust_street': self.cust_street,
            'cust_city': self.cust_city
        }
