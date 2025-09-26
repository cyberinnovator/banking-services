import mysql.connector
from mysql.connector import pooling, Error
from config import Config
import logging

class DatabaseConnection:
    _instance = None
    _connection_pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._connection_pool is None:
            try:
                self._connection_pool = pooling.MySQLConnectionPool(
                    pool_name="banking_pool",
                    pool_size=10,  # Adjust based on your needs
                    pool_reset_session=True,
                    host=Config.MYSQL_HOST,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    database=Config.MYSQL_DATABASE,
                    port=Config.MYSQL_PORT,
                    autocommit=True
                )
                logging.info("MySQL connection pool created")
            except Error as e:
                logging.error(f"Error creating connection pool: {e}")
                raise e
    
    def get_connection(self):
        try:
            return self._connection_pool.get_connection()
        except Error as e:
            logging.error(f"Error getting connection from pool: {e}")
            raise e
    
    def return_connection(self, connection):
        if connection and connection.is_connected():
            connection.close()  # This returns it to the pool

# Global database instance
db = DatabaseConnection()
