-- Seed Sample Data for Banking System
USE banking_system;

-- Insert sample customers
INSERT INTO Customer (cust_name, cust_street, cust_city) VALUES
('John Doe', '123 Main Street', 'New York'),
('Jane Smith', '456 Oak Avenue', 'Los Angeles'),
('Bob Johnson', '789 Pine Road', 'Chicago'),
('Alice Brown', '321 Elm Street', 'Houston'),
('Charlie Wilson', '654 Maple Drive', 'Phoenix');

-- Insert sample accounts
INSERT INTO Account (branch_name, balance, cust_id) VALUES
('Downtown Branch', 5000.00, 1),
('Uptown Branch', 3500.50, 2),
('Central Branch', 7200.75, 3),
('West Branch', 2100.25, 4),
('East Branch', 4800.00, 5),
('Downtown Branch', 1500.00, 1); -- John Doe's second account

-- Insert sample loans
INSERT INTO Loan (branch_name, amount, status, installments_remaining) VALUES
('Downtown Branch', 10000.00, 'approved', 24),
('Uptown Branch', 5000.00, 'pending', 12),
('Central Branch', 15000.00, 'approved', 36),
('West Branch', 8000.00, 'pending', 18);

-- Insert borrower relationships
INSERT INTO Borrower (cust_id, loan_no) VALUES
(1, 1), -- John Doe
(2, 2), -- Jane Smith
(3, 3), -- Bob Johnson
(4, 4); -- Alice Brown

-- Insert sample transactions
INSERT INTO Transaction (acc_no, type, amount, date_time) VALUES
-- Account 1 (John Doe - Downtown Branch)
(1, 'deposit', 1000.00, '2024-01-15 10:30:00'),
(1, 'withdrawal', 200.00, '2024-01-16 14:15:00'),
(1, 'deposit', 500.00, '2024-01-17 09:45:00'),

-- Account 2 (Jane Smith - Uptown Branch)
(2, 'deposit', 2000.00, '2024-01-15 11:00:00'),
(2, 'withdrawal', 150.00, '2024-01-18 16:30:00'),

-- Account 3 (Bob Johnson - Central Branch)
(3, 'deposit', 3000.00, '2024-01-14 08:20:00'),
(3, 'withdrawal', 500.00, '2024-01-19 13:10:00'),
(3, 'deposit', 1200.00, '2024-01-20 10:00:00'),

-- Account 4 (Alice Brown - West Branch)
(4, 'deposit', 1500.00, '2024-01-16 12:45:00'),
(4, 'withdrawal', 300.00, '2024-01-21 15:20:00'),

-- Account 5 (Charlie Wilson - East Branch)
(5, 'deposit', 2500.00, '2024-01-17 14:30:00'),
(5, 'withdrawal', 100.00, '2024-01-22 11:15:00'),

-- Account 6 (John Doe's second account)
(6, 'deposit', 800.00, '2024-01-18 09:30:00'),
(6, 'withdrawal', 50.00, '2024-01-23 16:45:00');

-- Display seeding status
SELECT 'Sample data inserted successfully!' as Status;

-- Display summary of inserted data
SELECT 
    (SELECT COUNT(*) FROM Customer) as Total_Customers,
    (SELECT COUNT(*) FROM Account) as Total_Accounts,
    (SELECT COUNT(*) FROM Loan) as Total_Loans,
    (SELECT COUNT(*) FROM Transaction) as Total_Transactions;
