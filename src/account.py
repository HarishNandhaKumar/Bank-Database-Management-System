import pymysql
import random
from datetime import datetime, timedelta


def prompt_for_positive_int(prompt_text):
    while True:
        try:
            amount = int(input(prompt_text))
            if amount > 0:
                return amount
        except ValueError:
            print("Invalid input. Please enter an amount > 0 and as an integer value.\n")


def prompt_for_valid_acc_number(prompt_text):
    while True:
        try:
            return int(input(prompt_text))
        except ValueError:
            print("Invalid input. Please enter a valid account number.")


def check_account_exists(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT acc_username FROM bank_account WHERE acc_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result is not None  # True if username exists
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return False


def get_user_branch_id(connection, username):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('get_user_branch_id', (username, None))
            cursor.execute("SELECT @_get_user_branch_id_1")
            result = cursor.fetchone()
            return int(result['@_get_user_branch_id_1'])

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None


def get_user_address_id(connection, username):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('get_account_user_address_id', (username, None))
            cursor.execute("SELECT @_get_account_user_address_id_1")
            result = cursor.fetchone()
            return int(result['@_get_account_user_address_id_1'])

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None


def check_acc_type(prompt_text):
    while True:
        try:
            acc_choice = int(input(prompt_text))
            if acc_choice == 1:
                acc_choice = "checking"
                return acc_choice
            elif acc_choice == 2:
                acc_choice = "savings"
                return acc_choice
            else:
                print("Invalid choice. Please enter a number 1 or number 2.\n")
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")


def generate_unique_account_number(connection):
    while True:
        account_number = random.randint(1000000000, 9999999999)
        try:
            with connection.cursor() as cursor:
                query = "SELECT COUNT(*) FROM bank_account WHERE acc_number = %s"
                cursor.execute(query, (account_number,))
                result = cursor.fetchone()
                if result['COUNT(*)'] == 0:
                    return account_number
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return None


def get_initial_deposit_amount():
    while True:
        try:
            amount = float(input("Enter an initial deposit amount (minimum 100USD): "))
            if amount >= 100:
                return amount
            else:
                print("Amount entered is less than minimum required. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid numeric value.")


def insert_create_new_account(connection, create_account_details):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('insert_create_new_account', create_account_details)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")


def generate_card_number(connection):
    while True:
        card_number = random.randint(100000000000, 999999999999)
        try:
            with connection.cursor() as cursor:
                query = "SELECT COUNT(*) FROM card WHERE card_number = %s"
                cursor.execute(query, (card_number,))
                result = cursor.fetchone()
                if result['COUNT(*)'] == 0:
                    return card_number
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return None


def generate_card_cvv_number(connection):
    while True:
        cvv_number = random.randint(000, 999)
        try:
            with connection.cursor() as cursor:
                query = "SELECT COUNT(*) FROM card WHERE cvv_number = %s"
                cursor.execute(query, (cvv_number,))
                result = cursor.fetchone()
                if result['COUNT(*)'] == 0:
                    return cvv_number
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return None


def insert_card_details(connection, new_card_details):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('insert_card_details', new_card_details)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")


def insert_debit_card_details(connection, new_dc_card_table_details):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('insert_debit_card_details', new_dc_card_table_details)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")


def insert_credit_card_details(connection, new_cc_card_table_details):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('insert_credit_card_details', new_cc_card_table_details)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")


def generate_debit_card(connection, account_number, user_branch_id, username, acc_initial_deposit):
    debit_card_number = generate_card_number(connection)
    card_acc_number = account_number
    card_branch_id = user_branch_id
    dc_card_type = "debit"
    card_holder_name = username
    dc_cvv_number = generate_card_cvv_number(connection)
    dc_card_issued_date = datetime.now().strftime('%Y-%m-%d')
    current_date = datetime.now()
    expiry_date = current_date + timedelta(days=5 * 365)
    dc_card_expiry_date = expiry_date.strftime('%Y-%m-%d')
    dc_daily_limit = 50000
    dc_balance = acc_initial_deposit
    new_debit_card_details = (debit_card_number, card_acc_number, card_branch_id, dc_card_type,
                              card_holder_name, dc_cvv_number, dc_card_issued_date, dc_card_expiry_date)
    new_dc_card_table_details = (debit_card_number, dc_daily_limit, dc_balance)
    insert_card_details(connection, new_debit_card_details)
    insert_debit_card_details(connection, new_dc_card_table_details)
    print(f"*** YOUR DEBIT CARD DETAILS: ***\n"
          f"debit card number: {debit_card_number}\n"
          f"debit card cvv number: {dc_cvv_number}\n"
          f"card holder name: {card_holder_name}\n"
          f"card_issued_date: {dc_card_issued_date}\n"
          f"card_expiry_date: {dc_card_expiry_date}\n"
          f"daily card limit: {dc_daily_limit}\n"
          f"card_balance: {dc_balance}\n")


def generate_credit_card(connection, account_number, user_branch_id, username):
    credit_card_number = generate_card_number(connection)
    card_acc_number = account_number
    card_branch_id = user_branch_id
    cc_card_type = "credit"
    card_holder_name = username
    cc_cvv_number = generate_card_cvv_number(connection)
    cc_card_issued_date = datetime.now().strftime('%Y-%m-%d')
    current_date = datetime.now()
    expiry_date = current_date + timedelta(days=5 * 365)
    cc_card_expiry_date = expiry_date.strftime('%Y-%m-%d')
    cc_interest_rate = 5
    cc_credit_used = 0
    cc_credit_available = 50000
    cc_credit_limit = 50000
    new_credit_card_details = (credit_card_number, card_acc_number, card_branch_id, cc_card_type,
                               card_holder_name, cc_cvv_number, cc_card_issued_date, cc_card_expiry_date)
    new_cc_card_table_details = (credit_card_number, cc_interest_rate, cc_credit_used, cc_credit_available,
                                 cc_credit_limit)
    insert_card_details(connection, new_credit_card_details)
    insert_credit_card_details(connection, new_cc_card_table_details)
    print(f"*** YOUR CREDIT CARD DETAILS: ***\n"
          f"credit card number: {credit_card_number}\n"
          f"credit card cvv number: {cc_cvv_number}\n"
          f"card holder name: {card_holder_name}\n"
          f"card_issued_date: {cc_card_issued_date}\n"
          f"card_expiry_date: {cc_card_expiry_date}\n"
          f"card interest rate: {cc_interest_rate}\n"
          f"credit used: {cc_credit_used}\n"
          f"credit available: {cc_credit_available}\n"
          f"credit limit (fixed): {cc_credit_limit}\n")


def get_current_account_balance(connection, acc_details):
    try:
        with connection.cursor() as cursor:
            user_curr_acc = acc_details + (0,)
            cursor.callproc('get_current_account_balance', user_curr_acc)
            cursor.execute("SELECT @_get_current_account_balance_2")
            result = cursor.fetchone()

            return int(result['@_get_current_account_balance_2'])

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None


def get_debit_card_number(connection, acc_number):
    try:
        with connection.cursor() as cursor:
            user_acc_number = acc_number + (0,)
            cursor.callproc('get_debit_card_number', user_acc_number)
            cursor.execute("SELECT @_get_debit_card_number_1")
            result = cursor.fetchone()
            return int(result['@_get_debit_card_number_1'])

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None


def update_current_account_balance(connection, acc_number, username, new_balance):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('update_current_account_balance', (acc_number, username, new_balance))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")


def update_debit_card_balance(connection, db_card_number, db_new_balance):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('update_debit_card_balance', (db_card_number, db_new_balance))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")


def record_deposit_transaction(connection, acc_number, t_type, t_date, t_amount, t_cur_type, t_before_balance,
                               t_balance_after, sender_acc_id, t_status):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('record_deposit_transaction',
                            (acc_number, t_type, t_date, t_amount, t_cur_type, t_before_balance, t_balance_after,
                             sender_acc_id, t_status))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")


def create_account(connection, username):
    if check_account_exists(connection, username):
        print("Bank Account already exist with this username!\n")
        return
    print("Please enter the following details to create account!\n")
    acc_type = check_acc_type("\nEnter your preferred account type from the following:\n"
                              "1. Checking Account\n"
                              "2. Savings Account\n"
                              "Your choice number:")

    print("\nEnter the initial amount to deposit\n")
    user_branch_id = get_user_branch_id(connection, username)
    user_address_id = get_user_address_id(connection, username)
    currency_type = "USD"
    account_number = generate_unique_account_number(connection)
    account_status = "active"
    acc_start_date = datetime.now().strftime('%Y-%m-%d')
    acc_initial_deposit = get_initial_deposit_amount()
    create_account_details = (account_number, username, user_address_id, user_branch_id,
                              acc_type, acc_initial_deposit, currency_type, acc_start_date, account_status)
    insert_create_new_account(connection, create_account_details)
    print(f"\nNEW ACCOUNT CREATED:\n"
          f"YOUR ACCOUNT NUMBER: {account_number}\n"
          f"YOUR CURRENT BALANCE: {acc_initial_deposit}\n"
          )

    print("\nGENERATING A DEBIT AND CREDIT CARD FOR NEW USER!\n")
    print("\nCONGRATS! SUCCESSFULLY GENERATED DEBIT AND CREDIT CARD!\n")
    generate_debit_card(connection, account_number, user_branch_id, username, acc_initial_deposit)
    generate_credit_card(connection, account_number, user_branch_id, username)
    t_type = "deposit"
    t_status = "completed"
    t_cur_type = "USD"
    t_date = datetime.now().strftime('%Y-%m-%d')
    t_initial_cur_bal = 0
    record_deposit_transaction(connection, account_number, t_type, t_date, acc_initial_deposit, t_cur_type,
                               t_initial_cur_bal, acc_initial_deposit, account_number, t_status)
    return


def deposit_amount(connection, username):
    if check_account_exists(connection, username) is False:
        print("No Bank Account exist with this username! Cannot proceed with transaction\n"
              "Please create a bank account to initiate the transaction\n")
        return
    print("\n**ENTER THE DETAILS TO INITIATE DEPOSIT**\n")
    acc_username = username
    acc_number = prompt_for_valid_acc_number("Enter your account number:\n")
    amount_to_deposit = prompt_for_positive_int("Enter the amount to deposit:\n")
    acc_details = (acc_username, acc_number)
    current_acc_bal = get_current_account_balance(connection, acc_details)
    new_acc_balance = current_acc_bal + amount_to_deposit
    acc_tuple = (acc_number,)
    db_card_number = get_debit_card_number(connection, acc_tuple)
    update_current_account_balance(connection, acc_number, username, new_acc_balance)
    update_debit_card_balance(connection, db_card_number, new_acc_balance)
    t_type = "deposit"
    t_status = "completed"
    t_cur_type = "USD"
    t_date = datetime.now().strftime('%Y-%m-%d')
    record_deposit_transaction(connection, acc_number, t_type, t_date, amount_to_deposit, t_cur_type, current_acc_bal,
                               new_acc_balance, acc_number, t_status)
    print(f"\nAMOUNT DEPOSITED SUCCESSFULLY\n"
          f"DEPOSITED ACCOUNT NUMBER: {acc_number}\n"
          f"INITIAL BALANCE: {current_acc_bal} USD\n"
          f"DEPOSITED AMOUNT: {amount_to_deposit} USD\n"
          f"NEW BALANCE: {new_acc_balance}")
    return
