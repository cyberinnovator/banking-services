-- Create Banking System Database
CREATE DATABASE IF NOT EXISTS banking_system;
USE banking_system;

-- Create Customer table
CREATE TABLE IF NOT EXISTS Customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_name VARCHAR(100) NOT NULL,
    cust_street VARCHAR(200),
    cust_city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Account table
CREATE TABLE IF NOT EXISTS Account (
    acc_no INT AUTO_INCREMENT PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    cust_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE,
    INDEX idx_customer (cust_id),
    INDEX idx_branch (branch_name)
);

-- Create Loan table
CREATE TABLE IF NOT EXISTS Loan (
    loan_no INT AUTO_INCREMENT PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    installments_remaining INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_branch (branch_name)
);

-- Create Borrower table (relationship between Customer and Loan)
CREATE TABLE IF NOT EXISTS Borrower (
    cust_id INT NOT NULL,
    loan_no INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (cust_id, loan_no),
    FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE,
    FOREIGN KEY (loan_no) REFERENCES Loan(loan_no) ON DELETE CASCADE
);

-- Create Transaction table
CREATE TABLE IF NOT EXISTS Transaction (
    txn_id INT AUTO_INCREMENT PRIMARY KEY,
    acc_no INT NOT NULL,
    type ENUM('deposit', 'withdrawal', 'transfer_in', 'transfer_out') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (acc_no) REFERENCES Account(acc_no) ON DELETE CASCADE,
    INDEX idx_account (acc_no),
    INDEX idx_type (type),
    INDEX idx_date (date_time)
);

-- Add constraints and triggers for data integrity
DELIMITER //

-- Trigger to prevent negative account balance
CREATE TRIGGER prevent_negative_balance 
BEFORE UPDATE ON Account 
FOR EACH ROW 
BEGIN 
    IF NEW.balance < 0 THEN 
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account balance cannot be negative'; 
    END IF; 
END//

-- Trigger to validate transaction amounts
CREATE TRIGGER validate_transaction_amount 
BEFORE INSERT ON Transaction 
FOR EACH ROW 
BEGIN 
    IF NEW.amount <= 0 THEN 
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Transaction amount must be positive'; 
    END IF; 
END//

DELIMITER ;

-- Create indexes for better performance
CREATE INDEX idx_customer_name ON Customer(cust_name);
CREATE INDEX idx_account_balance ON Account(balance);
CREATE INDEX idx_loan_amount ON Loan(amount);
CREATE INDEX idx_transaction_amount ON Transaction(amount);

-- Display table creation status
SELECT 'Database and tables created successfully!' as Status;
