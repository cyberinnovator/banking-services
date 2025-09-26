#!/usr/bin/env python3
"""
Database Setup Script for Banking System
This script creates the database, tables, and inserts sample data.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def read_sql_file(file_path):
    """Read SQL file and return its content"""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: SQL file '{file_path}' not found")
        return None

def execute_sql_script(cursor, sql_script, script_name):
    """Execute SQL script with proper error handling"""
    try:
        # Split the script into individual statements
        statements = sql_script.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                cursor.execute(statement)
        
        print(f"✓ {script_name} executed successfully")
        return True
    except Error as e:
        print(f"✗ Error executing {script_name}: {e}")
        return False

def setup_database():
    """Main function to set up the database"""
    print("🏦 Banking System Database Setup")
    print("=" * 40)
    
    # Database connection parameters
    config = {
        'host': os.environ.get('MYSQL_HOST', 'localhost'),
        'user': os.environ.get('MYSQL_USER', 'root'),
        'password': os.environ.get('MYSQL_PASSWORD', ''),
        'port': int(os.environ.get('MYSQL_PORT', 3306)),
        'autocommit': True
    }
    
    try:
        # Connect to MySQL server (without specifying database)
        print("📡 Connecting to MySQL server...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("✓ Connected to MySQL server successfully")
        
        # Read and execute database creation script
        print("\n📋 Creating database and tables...")
        create_script = read_sql_file('scripts/create_database.sql')
        if create_script:
            if execute_sql_script(cursor, create_script, "Database Creation Script"):
                print("✓ Database and tables created successfully")
            else:
                print("✗ Failed to create database and tables")
                return False
        else:
            print("✗ Could not read database creation script")
            return False
        
        # Read and execute sample data script
        print("\n📊 Inserting sample data...")
        seed_script = read_sql_file('scripts/seed_sample_data.sql')
        if seed_script:
            if execute_sql_script(cursor, seed_script, "Sample Data Script"):
                print("✓ Sample data inserted successfully")
            else:
                print("⚠️  Warning: Failed to insert sample data (database still functional)")
        else:
            print("⚠️  Warning: Could not read sample data script")
        
        # Verify setup
        print("\n🔍 Verifying database setup...")
        cursor.execute("USE banking_system")
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✓ Found {len(tables)} tables: {', '.join([table[0] for table in tables])}")
        
        # Check sample data
        cursor.execute("SELECT COUNT(*) FROM Customer")
        customer_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Account")
        account_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Loan")
        loan_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Transaction")
        transaction_count = cursor.fetchone()[0]
        
        print(f"✓ Sample data: {customer_count} customers, {account_count} accounts, {loan_count} loans, {transaction_count} transactions")
        
        print("\n🎉 Database setup completed successfully!")
        print("\n📝 Next steps:")
        print("1. Update your .env file with the correct database credentials")
        print("2. Install Python dependencies: pip install -r requirements.txt")
        print("3. Run the Flask application: python app.py")
        print("4. Test the API endpoints using a tool like Postman or curl")
        
        return True
        
    except Error as e:
        print(f"✗ Database connection error: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure MySQL server is running")
        print("2. Check your database credentials in the .env file")
        print("3. Ensure the MySQL user has sufficient privileges")
        return False
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n📡 MySQL connection closed")

if __name__ == "__main__":
    success = setup_database()
    exit(0 if success else 1)
