CREATE DATABASE IF NOT EXISTS bank_db_project;
USE bank_db_project;

CREATE TABLE bank_branch (
        branchId INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        bankname VARCHAR(100) NOT NULL,
        branchname VARCHAR(100) NOT NULL,
        b_st_number INT NOT NULL,
        b_street VARCHAR(100) NOT NULL,
        b_town VARCHAR(100) NOT NULL,
        b_city VARCHAR(100) NOT NULL,
        b_state VARCHAR(100) NOT NULL,
        b_zip INT NOT NULL,
        b_ph_number CHAR(10) NOT NULL CHECK (b_ph_number REGEXP '^[0-9]{10}$')
        );
        
CREATE TABLE customer_address (
        c_addressId INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        c_st_number INT NOT NULL,
        c_street VARCHAR(100) NOT NULL,
        c_town VARCHAR(100) NOT NULL,
        c_city VARCHAR(100) NOT NULL,
        c_state VARCHAR(100) NOT NULL,
        c_zip INT NOT NULL
        );
        
CREATE TABLE customer (
	    c_username VARCHAR(20) NOT NULL PRIMARY KEY,
        c_address_id INT,
        c_branch_id INT,
        c_password VARCHAR(20) NOT NULL,
        c_first_name VARCHAR(100) NOT NULL,
        c_last_name VARCHAR(100) NOT NULL,
        c_age INT NOT NULL,
        c_dob DATE NOT NULL,
        c_gender ENUM ('male', 'female', 'transgender') NOT NULL,
        c_phone_number INT NOT NULL,
        c_ssn INT NOT NULL,
        FOREIGN KEY (c_address_id) REFERENCES customer_address (c_addressId) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (c_branch_id) REFERENCES bank_branch (branchId) ON UPDATE CASCADE ON DELETE CASCADE
        );
        
CREATE TABLE bank_account (
		acc_number BIGINT NOT NULL UNIQUE PRIMARY KEY,
        acc_username VARCHAR(20) NOT NULL,
        acc_user_addressId INT NOT NULL,
        acc_branchId INT NOT NULL,
        acc_type ENUM ('checking', 'savings'),
        acc_balance INT NOT NULL DEFAULT 0,
        currency_type VARCHAR(5) NOT NULL,
        acc_start_date DATETIME NOT NULL,
        acc_end_date DATETIME DEFAULT NULL,
        acc_status ENUM ('active', 'closed'),
        FOREIGN KEY (acc_username) REFERENCES customer (c_username) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (acc_user_addressId) REFERENCES customer_address (c_addressId) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (acc_branchId) REFERENCES bank_branch (branchId) ON UPDATE CASCADE ON DELETE CASCADE
        );

CREATE TABLE transactions (
        transactionId INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
        t_acc_number BIGINT NOT NULL,
        t_type ENUM ('deposit', 'withdrawal', 'transfer', 'credit'),
        t_date DATETIME NOT NULL,
        t_amount INT NOT NULL,
        t_currency_type VARCHAR(5) NOT NULL,
        t_balance_before INT NOT NULL,
        t_balance_after INT NOT NULL,
        sender_acc_id BIGINT NOT NULL,
        receiver_acc_id BIGINT DEFAULT NULL,
        t_status ENUM ('transit', 'completed'),
        FOREIGN KEY (t_acc_number) REFERENCES bank_account (acc_number) ON UPDATE CASCADE ON DELETE CASCADE
        );
        
CREATE TABLE card (
        card_number BIGINT NOT NULL UNIQUE PRIMARY KEY,
        card_acc_num BIGINT NOT NULL,
        card_branch_id INT NOT NULL,
        card_type ENUM ('debit', 'credit'),
        card_holder_name VARCHAR(50) NOT NULL,
        cvv_number INT NOT NULL,
        issued_date DATETIME NOT NULL,
        expiry_date DATETIME NOT NULL,
        FOREIGN KEY (card_acc_num) REFERENCES bank_account (acc_number) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (card_branch_id) REFERENCES bank_branch (branchId) ON UPDATE CASCADE ON DELETE CASCADE
        );
        
CREATE TABLE debit_card (
        dc_number BIGINT NOT NULL UNIQUE PRIMARY KEY,
        daily_limit INT NOT NULL,
        dc_balance INT NOT NULL DEFAULT 0,
        FOREIGN KEY (dc_number) REFERENCES card (card_number) ON UPDATE CASCADE ON DELETE CASCADE
        );
        
CREATE TABLE credit_card (
        cc_number BIGINT NOT NULL UNIQUE PRIMARY KEY,
        interest_rate INT NOT NULL,
        credit_used INT NOT NULL DEFAULT 0,
        credit_available INT NOT NULL,
        credit_limit INT NOT NULL,
        FOREIGN KEY (cc_number) REFERENCES card (card_number) ON UPDATE CASCADE ON DELETE CASCADE
        );
        
CREATE TABLE loan (
        loan_number INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
        loan_bank_id INT NOT NULL,
        customer_username VARCHAR(20) NOT NULL,
        loan_type ENUM ('personal', 'education', 'business'),
        total_loan_amt INT NOT NULL,
        loan_balance INT NOT NULL,
        loan_duration INT NOT NULL,
        loan_interest INT NOT NULL,
        FOREIGN KEY (loan_bank_id) REFERENCES bank_branch (branchId) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (customer_username) REFERENCES customer (c_username) ON UPDATE CASCADE ON DELETE CASCADE
        );
	
CREATE TABLE investment (
        investment_number INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
        inv_bank_id INT NOT NULL,
        customer_username VARCHAR(20) NOT NULL,
        investment_type ENUM ('stocks', 'bonds', 'mutual funds'),
        invested_amount INT NOT NULL,
        inv_risk_level ENUM ('low',  'medium', 'high'),
        investemnt_term INT NOT NULL,
		FOREIGN KEY (inv_bank_id) REFERENCES bank_branch (branchId) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (customer_username) REFERENCES customer (c_username) ON UPDATE CASCADE ON DELETE CASCADE
        );
        
CREATE TABLE insurance (
        insurance_number INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
        ins_bank_id INT NOT NULL,
        customer_username VARCHAR(20) NOT NULL,
        insurance_type ENUM ('life', 'health', 'auto', 'home'),
        coverage_amount INT NOT NULL,
        policy_term INT NOT NULL,
        policy_status ENUM ('active', 'terminated'),
        FOREIGN KEY (ins_bank_id) REFERENCES bank_branch (branchId) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (customer_username) REFERENCES customer (c_username) ON UPDATE CASCADE ON DELETE CASCADE
        );

/* INSETING THE BANK BRANCH DETAILS INTO bank_branch table */
INSERT INTO bank_branch 
(bankname, branchname, b_st_number, b_street, b_town, b_city, b_state, b_zip, b_ph_number) 
VALUES ('Boston Bank', 'Downtown', 123, 'Main Street', 'Old Town', 'Springfield', 'Illinois', 62701, 2175551234),
('Boston Bank', 'Uptown', 456, 'Market Avenue', 'West Side', 'Chicago', 'Illinois', 60616, 3125555678),
('Boston Bank', 'Northside', 789, 'Elm Drive', 'North Village', 'Peoria', 'Illinois', 61614, 3095557890),
('Boston Bank', 'Eastside', 101, 'Oak Lane', 'East Point', 'Decatur', 'Illinois', 62522, 2175554567);        
        
        
        
        
        
        
        
        
        
        
        
        