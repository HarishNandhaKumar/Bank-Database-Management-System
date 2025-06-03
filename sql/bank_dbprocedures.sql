USE bank_db_project;

DELIMITER $$
CREATE PROCEDURE register_user_details(
    IN p_username VARCHAR(20),
    IN p_password VARCHAR(20),
    IN p_first_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_age INT,
    IN p_dob DATETIME,
    IN p_gender ENUM('male', 'female', 'transgender'),
    IN p_phone_number INT,
    IN p_ssn INT,
    IN p_branch_id INT
)
BEGIN

    INSERT INTO customer (
        c_username, c_password, c_first_name, c_last_name,
        c_age, c_dob, c_gender, c_phone_number, c_ssn, c_branch_id
    ) VALUES (
        p_username, p_password, p_first_name, p_last_name,
        p_age, p_dob, p_gender, p_phone_number, p_ssn, p_branch_id
    );
    
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE register_user_address(
        IN u_st_number INT,
        IN u_street VARCHAR(100),
        IN u_town VARCHAR(100),
        IN u_city VARCHAR(100),
        IN u_state VARCHAR(100),
        IN u_zip INT
)
BEGIN 
    
    INSERT INTO customer_address (
		c_st_number, c_street, c_town, c_city, c_state, c_zip 
        ) VALUES (
		u_st_number, u_street, u_town, u_city, u_state, u_zip
        );

END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE get_user_address_id(
        IN u_st_number INT,
        IN u_street VARCHAR(100),
        IN u_town VARCHAR(100),
        IN u_city VARCHAR(100),
        IN u_state VARCHAR(100),
        IN u_zip INT,
        OUT address_id INT
)
BEGIN
     SELECT c_addressId
     INTO address_id 
     FROM customer_address
     WHERE c_st_number = u_st_number AND c_street = u_street AND c_town = u_town
	 AND c_city = u_city AND c_state = u_state AND c_zip = u_zip
     LIMIT 1;
     
     IF address_id IS NULL THEN
        SET address_id = -1;
    END IF;
    
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE insert_customer_address_id(
    IN user_address_id INT,
    IN p_username VARCHAR(100)
)
BEGIN
    UPDATE customer
	SET c_address_id = user_address_id
	WHERE c_username = p_username;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE get_user_branch_id(
        IN p_username VARCHAR(100),
        OUT p_branch_id INT
)
BEGIN
     SELECT c_branch_id
     INTO p_branch_id
     FROM customer
     WHERE c_username = p_username
     LIMIT 1;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE get_account_user_address_id(
        IN p_username VARCHAR(100),
        OUT p_account_id INT
)
BEGIN
     SELECT c_address_id
     INTO p_account_id
     FROM customer
     WHERE c_username = p_username
     LIMIT 1;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE insert_create_new_account(
    IN p_acc_num BIGINT,
    IN p_username VARCHAR(100),
    IN p_address_id INT,
    IN p_bank_branch_id INT,
    IN p_acc_type VARCHAR(20),
    IN p_acc_deposit INT,
    IN p_cur_type VARCHAR(10),
    IN p_acc_start_date DATETIME,
    IN acc_status VARCHAR(10)
)
BEGIN
    INSERT INTO bank_account (
		acc_number, acc_username, acc_user_addressId, acc_branchId, acc_type, acc_balance, currency_type,
        acc_start_date, acc_status
        ) VALUES (
		p_acc_num, p_username, p_address_id, p_bank_branch_id, p_acc_type, p_acc_deposit, p_cur_type,
        p_acc_start_date, acc_status
        );
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE insert_card_details(
       IN p_card_number BIGINT,
       IN p_card_acc_number BIGINT,
       IN p_card_branch_number INT,
       IN p_card_type VARCHAR(10),
       IN p_card_holder_name VARCHAR(100),
       IN p_cvv_number INT,
       IN p_issued_date DATETIME,
       IN p_expiry_date DATETIME
)
BEGIN
    INSERT INTO card (
		card_number, card_acc_num, card_branch_id, card_type, card_holder_name, cvv_number,
        issued_date, expiry_date
        ) VALUES (
		p_card_number, p_card_acc_number, p_card_branch_number, p_card_type, p_card_holder_name,
        p_cvv_number, p_issued_date, p_expiry_date
        );
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE insert_debit_card_details(
       IN p_dc_card_number BIGINT,
       IN p_daily_limit INT,
       IN p_balance INT
)
BEGIN
    INSERT INTO debit_card (
		dc_number, daily_limit, dc_balance
        ) VALUES (
		p_dc_card_number, p_daily_limit, p_balance
        );
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE insert_credit_card_details(
       IN p_cc_card_number BIGINT,
       IN p_interest_rate INT,
       IN p_credit_used INT,
       IN p_credit_available INT,
       IN p_credit_limit INT
)
BEGIN
    INSERT INTO credit_card (
		cc_number, interest_rate, credit_used, credit_available, credit_limit
        ) VALUES (
		p_cc_card_number , p_interest_rate, p_credit_used, p_credit_available, p_credit_limit
        );
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE get_current_account_balance(
        IN p_username VARCHAR(100),
        IN p_acc_number BIGINT,
        OUT p_cur_balance INT
)
BEGIN
     SELECT acc_balance
     INTO p_cur_balance 
     FROM bank_account
     WHERE acc_number = p_acc_number AND acc_username = p_username
     LIMIT 1;
     
     IF p_cur_balance IS NULL THEN
        SET p_cur_balance = 0;
    END IF;
    
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE get_debit_card_number(
      IN p_acc_number BIGINT,
      OUT p_debit_card_number BIGINT
)
BEGIN 
      SELECT dc_number
      INTO p_debit_card_number
      FROM debit_card
      JOIN card ON card.card_number = debit_card.dc_number
      WHERE card.card_acc_num = p_acc_number
      LIMIT 1;

END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE update_current_account_balance(
	  IN p_acc_number BIGINT,
      IN p_username VARCHAR(100),
      IN dc_new_balance INT
)
BEGIN 
      UPDATE bank_account
      SET acc_balance = dc_new_balance
      WHERE acc_number = p_acc_number AND acc_username = p_username;

END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE update_debit_card_balance(
    IN dc_card_number BIGINT,
    IN dc_new_balance INT
)
BEGIN 
    IF EXISTS (SELECT 1 FROM debit_card WHERE dc_number = dc_card_number) THEN
        UPDATE debit_card
        SET dc_balance = dc_new_balance
        WHERE dc_number = dc_card_number;
    ELSE
        SELECT 'Card number does not exist' AS Error;
    END IF;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE record_deposit_transaction(
       IN ts_acc_number BIGINT, 
       IN ts_type VARCHAR(20), 
       IN ts_date DATETIME,
       IN ts_amount INT, 
       IN ts_cur_type VARCHAR(10), 
       IN ts_cur_bal INT,
       IN ts_new_bal INT,
       IN ts_sender_acc_number BIGINT,
       IN ts_status VARCHAR(20)
)
BEGIN
      INSERT INTO transactions(
		t_acc_number, t_type, t_date, t_amount, t_currency_type, t_balance_before, t_balance_after,
        sender_acc_id, t_status
        ) VALUES (
		ts_acc_number, ts_type, ts_date, ts_amount, ts_cur_type, ts_cur_bal, ts_new_bal, ts_sender_acc_number,
        ts_status
        );
        
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE get_account_number(
         IN p_username VARCHAR(100),
         OUT p_acc_number BIGINT
)
BEGIN 
      SELECT acc_number
      INTO p_acc_number
      FROM bank_account
      WHERE acc_username = p_username
      LIMIT 1;

END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE get_username_from_bank_account(
         IN p_acc_num BIGINT,
         OUT p_username VARCHAR(100)
)
BEGIN 
      SELECT acc_username
      INTO p_username
      FROM bank_account
      WHERE acc_number = p_acc_num
      LIMIT 1;

END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE record_account_transaction(
       IN ts_acc_number BIGINT, 
       IN ts_type VARCHAR(20), 
       IN ts_date DATETIME,
       IN ts_amount INT, 
       IN ts_cur_type VARCHAR(10), 
       IN ts_cur_bal INT,
       IN ts_new_bal INT,
       IN ts_sender_acc_number BIGINT,
       IN ts_receiver_acc_number BIGINT,
       IN ts_status VARCHAR(20)
)
BEGIN
      INSERT INTO transactions(
		t_acc_number, t_type, t_date, t_amount, t_currency_type, t_balance_before, t_balance_after,
        sender_acc_id, receiver_acc_id, t_status
        ) VALUES (
		ts_acc_number, ts_type, ts_date, ts_amount, ts_cur_type, ts_cur_bal, ts_new_bal, ts_sender_acc_number,
        ts_receiver_acc_number, ts_status
        );
        
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE get_credit_card_number(
      IN p_acc_number BIGINT,
      OUT p_credit_card_number BIGINT
)
BEGIN 
      SELECT cc_number
      INTO p_credit_card_number
      FROM credit_card
      JOIN card ON card.card_number = credit_card.cc_number
      WHERE card.card_acc_num = p_acc_number
      LIMIT 1;

END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE get_credit_card_limit(
	  IN p_credit_card_num BIGINT,
      OUT p_card_limit INT
)
BEGIN
     SELECT credit_limit
     INTO p_card_limit
     FROM credit_card
     WHERE cc_number = p_credit_card_num
     LIMIT 1;

END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE get_credit_card_available_credit(
	  IN p_credit_card_num BIGINT,
      OUT p_available_credit INT
)
BEGIN
     SELECT credit_available
     INTO p_available_credit
     FROM credit_card
     WHERE cc_number = p_credit_card_num
     LIMIT 1;

END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE get_credit_card_credit_used(
	  IN p_credit_card_num BIGINT,
      OUT p_credit_used INT
)
BEGIN
     SELECT credit_used
     INTO p_credit_used
     FROM credit_card
     WHERE cc_number = p_credit_card_num
     LIMIT 1;

END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE update_credit_card_balances(
    IN cc_card_number BIGINT,
    IN cc_credit_used INT,
    IN cc_credit_available INT
)
BEGIN 
    IF EXISTS (SELECT 1 FROM credit_card WHERE cc_number = cc_card_number) THEN
        UPDATE credit_card
        SET credit_used = cc_credit_used, credit_available = cc_credit_available
        WHERE cc_number = cc_card_number;
    ELSE
        SELECT 'Card number does not exist' AS Error;
    END IF;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE insert_new_loan(
      IN p_loan_bank_id INT,
      IN p_customer_username VARCHAR(100),
      IN p_loan_type VARCHAR(50),
      IN p_total_loan_amt INT,
      IN p_loan_balance INT,
      IN p_loan_duration INT,
      IN p_loan_interest INT
) 
BEGIN
      INSERT INTO loan(
		loan_bank_id, customer_username, loan_type, total_loan_amt, loan_balance, loan_duration,
        loan_interest
        ) VALUES (
		p_loan_bank_id, p_customer_username, p_loan_type, p_total_loan_amt, p_loan_balance, p_loan_duration,
        p_loan_interest
        );
        
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE update_loan_balance(
        IN p_loan_number INT,
        IN p_deducted_amount INT
)
BEGIN 
     IF EXISTS (SELECT 1 FROM loan WHERE loan_number = p_loan_number) THEN
        UPDATE loan
        SET loan_balance = p_deducted_amount
        WHERE loan_number = p_loan_number;
    ELSE
        SELECT 'Loan does not exist' AS Error;
    END IF;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE delete_loan(
    IN loan_id INT
)
BEGIN

    DELETE FROM loan
    WHERE loan_number = loan_id;

    CREATE TEMPORARY TABLE temp_table AS
    SELECT ROW_NUMBER() OVER (ORDER BY loan_number) AS new_loan_number, loan_number
    FROM loan;

    UPDATE loan
    INNER JOIN temp_table
    ON loan.loan_number = temp_table.loan_number
    SET loan.loan_number = temp_table.new_loan_number;

    DROP TEMPORARY TABLE temp_table;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE add_investment(
     IN p_inv_bank_id INT,
     IN p_customer_username VARCHAR(100),
     IN p_investment_type VARCHAR(50),
     IN p_invested_amount INT,
     IN p_inv_risk_level VARCHAR(20),
     IN p_investemnt_term INT
) 
BEGIN 
     INSERT INTO investment(
		inv_bank_id, customer_username, investment_type, invested_amount,
        inv_risk_level, investemnt_term
        ) VALUES (
		p_inv_bank_id, p_customer_username, p_investment_type, p_invested_amount,
        p_inv_risk_level, p_investemnt_term
        );

END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE delete_investment(
    IN inv_username VARCHAR(100)
)
BEGIN

    DELETE FROM investment
    WHERE customer_username = inv_username;

    CREATE TEMPORARY TABLE temp_table AS
    SELECT ROW_NUMBER() OVER (ORDER BY customer_username) AS new_inv_c_name, customer_username
    FROM investment;

    UPDATE investment
    INNER JOIN temp_table
    ON investment.customer_username = temp_table.customer_username
    SET investment.customer_username = temp_table.new_inv_c_name;

    DROP TEMPORARY TABLE temp_table;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE add_insurance(
     IN p_ins_bank_id INT,
     IN p_customer_username VARCHAR(100),
     IN p_insurance_type VARCHAR(50),
     IN p_coverage_amount INT,
     IN p_policy_term INT,
     IN p_policy_status VARCHAR(50)
) 
BEGIN 
     INSERT INTO insurance(
		ins_bank_id, customer_username, insurance_type, coverage_amount,
        policy_term, policy_status
        ) VALUES (
		p_ins_bank_id, p_customer_username, p_insurance_type, p_coverage_amount,
        p_policy_term, p_policy_status
        );

END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE delete_insurance(
    IN ins_username VARCHAR(100)
)
BEGIN

    DELETE FROM insurance
    WHERE customer_username = ins_username;

    CREATE TEMPORARY TABLE temp_table AS
    SELECT ROW_NUMBER() OVER (ORDER BY customer_username) AS new_ins_c_name, customer_username
    FROM insurance;

    UPDATE insurance
    INNER JOIN temp_table
    ON insurance.customer_username = temp_table.customer_username
    SET insurance.customer_username = temp_table.new_ins_c_name;

    DROP TEMPORARY TABLE temp_table;
END $$
DELIMITER ;







