from account import *

from transaction import get_acc_number


def check_valid_inv_choice(prompt_text):
    while True:
        try:
            inv_choice = int(input(prompt_text))
            if 1 <= inv_choice <= 3:
                return int(inv_choice)
            else:
                print("Invalid investment choice. Please enter a number 1 or 2 or 3.\n")
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")


def check_inv_exists(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT customer_username FROM investment WHERE customer_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result is not None
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return False


def insert_new_inv(connection, inv_details):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('add_investment', inv_details)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")


def delete_investment_username(connection, inv_id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('delete_investment', (inv_id,))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")


def delete_investment(connection, username):
    if check_inv_exists(connection, username):
        delete_investment_username(connection, username)
        print(f"\nINVESTMENT DELETED SUCCESSFULLY for USERNAME:{username}\n")
        return
    else:
        print(f"\nNO INVESTMENT EXIST for USERNAME:{username}\n"
              f"DELETE OPERATION FAILED\n")
        return


def make_investment(connection, username):
    inv_username = username
    inv_bank_id = get_user_branch_id(connection, inv_username)
    if check_account_exists(connection, username) is False:
        print("\nNO BANK ACCOUNT FOUND WITH THIS USERNAME. CANNOT MAKE INVESTMENT WITHOUT ACCOUNT\n"
              "PLEASE CREATE BANK ACCOUNT FIRST AND MAKE INVESTMENT\n")
        return

    if check_inv_exists(connection, inv_username):
        print(f"\nUSERNAME {inv_username}, ALREADY HAVE AN INVESTMENT!. CANNOT CREATE ANOTHER INVESTMENT.\n")
        return

    while True:
        loan_choice = check_valid_inv_choice("\n** Apply for Investment **\n"
                                             "Choose the type of Investment:\n"
                                             "1. Stocks\n"
                                             "2. Bonds\n"
                                             "3. Mutual Funds\n"
                                             "Your choice: ")
        inv_amt = prompt_for_positive_int("\nEnter the investment amount: (Only Debit Payment)")
        if loan_choice == 1:
            get_stocks_inv(connection, inv_username, inv_bank_id, inv_amt)
            return
        elif loan_choice == 2:
            get_bonds_inv(connection, inv_username, inv_bank_id, inv_amt)
            return
        elif loan_choice == 3:
            get_mutual_funds_inv(connection, inv_username, inv_bank_id, inv_amt)
            return


def get_stocks_inv(connection, inv_username, inv_bank_id, inv_amt):
    user_acc_number = get_acc_number(connection, inv_username)
    user_acc_balance = get_current_account_balance(connection, (inv_username, user_acc_number))
    if inv_amt > user_acc_number:
        print("\nINSUFFICIENT ACCOUNT BALANCE!.\n"
              "PAYMENT CANCELLED\n")
        return
    new_acc_balance = user_acc_balance - inv_amt
    new_debit_balance = new_acc_balance
    db_card_number = get_debit_card_number(connection, (user_acc_number,))
    update_current_account_balance(connection, user_acc_number, inv_username, new_acc_balance)
    update_debit_card_balance(connection, db_card_number, new_debit_balance)
    t_date = datetime.now().strftime('%Y-%m-%d')
    record_deposit_transaction(connection, user_acc_number, "withdrawal", t_date, inv_amt, "USD",
                               user_acc_balance, new_acc_balance, user_acc_number, "completed")
    invest_bank_id = inv_bank_id
    inv_type = "stocks"
    inv_risk_level = "high"
    inv_term = 2
    inv_details = (invest_bank_id, inv_username, inv_type, inv_amt, inv_risk_level, inv_term)
    insert_new_inv(connection, inv_details)
    print(f"\nSTOCKS INVESTMENT UPDATED for USER {inv_username}\n")


def get_bonds_inv(connection, inv_username, inv_bank_id, inv_amt):
    user_acc_number = get_acc_number(connection, inv_username)
    user_acc_balance = get_current_account_balance(connection, (inv_username, user_acc_number))
    if inv_amt > user_acc_number:
        print("\nINSUFFICIENT ACCOUNT BALANCE!.\n"
              "PAYMENT CANCELLED\n")
        return
    new_acc_balance = user_acc_balance - inv_amt
    new_debit_balance = new_acc_balance
    db_card_number = get_debit_card_number(connection, (user_acc_number,))
    update_current_account_balance(connection, user_acc_number, inv_username, new_acc_balance)
    update_debit_card_balance(connection, db_card_number, new_debit_balance)
    t_date = datetime.now().strftime('%Y-%m-%d')
    record_deposit_transaction(connection, user_acc_number, "withdrawal", t_date, inv_amt, "USD",
                               user_acc_balance, new_acc_balance, user_acc_number, "completed")
    invest_bank_id = inv_bank_id
    inv_type = "bonds"
    inv_risk_level = "low"
    inv_term = 10
    inv_details = (invest_bank_id, inv_username, inv_type, inv_amt, inv_risk_level, inv_term)
    insert_new_inv(connection, inv_details)
    print(f"\nBONDS INVESTMENT UPDATED for USER {inv_username}\n")


def get_mutual_funds_inv(connection, inv_username, inv_bank_id, inv_amt):
    user_acc_number = get_acc_number(connection, inv_username)
    user_acc_balance = get_current_account_balance(connection, (inv_username, user_acc_number))
    if inv_amt > user_acc_number:
        print("\nINSUFFICIENT ACCOUNT BALANCE!.\n"
              "PAYMENT CANCELLED\n")
        return
    new_acc_balance = user_acc_balance - inv_amt
    new_debit_balance = new_acc_balance
    db_card_number = get_debit_card_number(connection, (user_acc_number,))
    update_current_account_balance(connection, user_acc_number, inv_username, new_acc_balance)
    update_debit_card_balance(connection, db_card_number, new_debit_balance)
    t_date = datetime.now().strftime('%Y-%m-%d')
    record_deposit_transaction(connection, user_acc_number, "withdrawal", t_date, inv_amt, "USD",
                               user_acc_balance, new_acc_balance, user_acc_number, "completed")
    invest_bank_id = inv_bank_id
    inv_type = "mutual funds"
    inv_risk_level = "medium"
    inv_term = 5
    inv_details = (invest_bank_id, inv_username, inv_type, inv_amt, inv_risk_level, inv_term)
    insert_new_inv(connection, inv_details)
    print(f"\nMUTUAL FUNDS INVESTMENT UPDATED for USER {inv_username}\n")
