

from transaction import *
from account import *
from register import *


def check_valid_loan_choice(prompt_text):
    while True:
        try:
            loan_choice = int(input(prompt_text))
            if 1 <= loan_choice <= 3:
                return int(loan_choice)
            else:
                print("Invalid loan choice. Please enter a number 1 or 2 or 3.\n")
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")


def check_loan_exists(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT customer_username FROM loan WHERE customer_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result is not None
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return False


def insert_new_loan(connection, loan_details):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('insert_new_loan', loan_details)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")


def get_loan_number(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT loan_number FROM loan WHERE customer_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result['loan_number']
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return 0


def get_loan_balance(connection, loan_id):
    try:
        with connection.cursor() as cursor:
            query = "SELECT loan_balance FROM loan WHERE loan_number = %s"
            cursor.execute(query, (loan_id,))
            result = cursor.fetchone()
            return result['loan_balance']
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return 0


def update_loan_balance(connection, loan_details):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('update_loan_balance', loan_details)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")


def delete_loan(connection, loan_id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('delete_loan', (loan_id,))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")


def pay_loan(connection, username):
    if check_account_exists(connection, username) is False:
        print("\nNO BANK ACCOUNT FOUND WITH THIS USERNAME. CANNOT MAKE LOAN PAYMENTS\n")
        return

    if check_loan_exists(connection, username) is False:
        print(f"\nNO LOAN EXIST FOR THIS USERNAME {username}\n")
        return
    loan_id = get_loan_number(connection, username)
    loan_balance_amt = get_loan_balance(connection, loan_id)
    amount_to_pay = prompt_for_positive_int("\nEnter the amount to pay: ")
    if amount_to_pay > loan_balance_amt:
        amount_to_pay = loan_balance_amt
    deducted_balance = loan_balance_amt - amount_to_pay
    if deducted_balance < 0:
        deducted_balance = 0

    payment_method_choice = check_valid_payment_choice("\n** Transfer amount to Loan Balance **\n"
                                                       "Enter your choice for payment method:\n"
                                                       "1. Debit Card payment\n"
                                                       "2. Credit Card payment\n"
                                                       "Your choice: ")

    if payment_method_choice == 1:
        user_acc_number = get_acc_number(connection, username)
        user_acc_balance = get_current_account_balance(connection, (username, user_acc_number))
        if amount_to_pay > user_acc_number:
            print("\nINSUFFICIENT ACCOUNT BALANCE!.\n"
                  "PAYMENT CANCELLED\n")
            return
        new_acc_balance = user_acc_balance - amount_to_pay
        new_debit_balance = new_acc_balance
        db_card_number = get_debit_card_number(connection, (user_acc_number,))
        update_current_account_balance(connection, user_acc_number, username, new_acc_balance)
        update_debit_card_balance(connection, db_card_number, new_debit_balance)
        loan_details = (loan_id, deducted_balance)
        update_loan_balance(connection, loan_details)
        t_date = datetime.now().strftime('%Y-%m-%d')
        record_deposit_transaction(connection, user_acc_number, "withdrawal", t_date, amount_to_pay, "USD",
                                   user_acc_balance, new_acc_balance, user_acc_number, "completed")
        if deducted_balance <= 0:
            delete_loan(connection, loan_id)
            print("\nLOAN COMPLETED, RECORD DELETED!\n")

        print(f"\nLOAN PAYMENT UPDATED FOR LOAN ID:{loan_id} for USER {username}\n")
        return

    elif payment_method_choice == 2:
        user_acc_number = get_acc_number(connection, username)
        cc_card_number = get_credit_card_num(connection, (user_acc_number,))
        cc_card_limit = get_credit_card_limit(connection, (cc_card_number,))
        cc_card_credit_used = get_used_credit(connection, (cc_card_number,))
        cc_available_credit = get_credit_available(connection, (cc_card_number,))
        if amount_to_pay > cc_available_credit:
            print(f"\nPAYMENT AMOUNT EXCEEDS CARD LIMIT, CARD LIMIT = {cc_card_limit}\n"
                  f"PAYMENT CANCELLED\n")
            return
        new_cc_available_credit = cc_available_credit - amount_to_pay
        new_cc_credit_used = cc_card_credit_used + amount_to_pay
        loan_details = (loan_id, deducted_balance)
        update_loan_balance(connection, loan_details)
        t_date = datetime.now().strftime('%Y-%m-%d')
        update_credit_card_balances(connection, cc_card_number, new_cc_credit_used, new_cc_available_credit)
        record_account_transaction(connection, user_acc_number, "credit", t_date, amount_to_pay, "USD",
                                   cc_available_credit, new_cc_available_credit, user_acc_number, user_acc_number,
                                   "completed")

        if deducted_balance <= 0:
            delete_loan(connection, loan_id)
            print("\nLOAN COMPLETED, RECORD DELETED!\n")

        print(f"\nLOAN PAYMENT UPDATED FOR LOAN ID:{loan_id} for USER {username}\n")
        return


def apply_loan(connection, username):
    loan_username = username
    loan_bank_id = get_user_branch_id(connection, loan_username)
    if check_account_exists(connection, username) is False:
        print("\nLOANS CANNOT BE PROCESSED WITHOUT BANK ACCOUNT. PLEASE CREATE BANK ACCOUNT TO PROCEED\n")
        return

    if check_loan_exists(connection, loan_username):
        print(f"\nUSERNAME {loan_username}, ALREADY HAVE A LOAN!. CANNOT APPLY ANOTHER LOAN.\n")
        return

    while True:
        loan_choice = check_valid_loan_choice("\n** Apply for Loan **\n"
                                              "Choose the type of Loan:\n"
                                              "1. Personal\n"
                                              "2. Education\n"
                                              "3. Business\n"
                                              "Your choice: ")
        loan_amt = prompt_for_positive_int("\nEnter the expected loan amount: ")
        if loan_choice == 1:
            get_personal_loan(connection, loan_username, loan_bank_id, loan_amt)
            print("\nCONGRATS, YOUR PERSONAL LOAN IS APPROVED.\n")
            return
        elif loan_choice == 2:
            get_education_loan(connection, loan_username, loan_bank_id, loan_amt)
            print("\nCONGRATS, YOUR EDUCATION LOAN IS APPROVED.\n")
            return
        elif loan_choice == 3:
            get_business_loan(connection, loan_username, loan_bank_id, loan_amt)
            print("\nCONGRATS, YOUR BUSINESS LOAN IS APPROVED.\n")
            return


def get_personal_loan(connection, loan_username, loan_bank_id, loan_amt):
    loan_type = "personal"
    total_loan_amt = loan_amt
    loan_balance = loan_amt
    loan_duration = 3
    loan_interest = 10
    loan_details = (loan_bank_id, loan_username, loan_type, total_loan_amt, loan_balance, loan_duration,
                    loan_interest)
    insert_new_loan(connection, loan_details)


def get_education_loan(connection, loan_username, loan_bank_id, loan_amt):
    loan_type = "education"
    total_loan_amt = loan_amt
    loan_balance = loan_amt
    loan_duration = 10
    loan_interest = 8
    loan_details = (loan_bank_id, loan_username, loan_type, total_loan_amt, loan_balance, loan_duration,
                    loan_interest)
    insert_new_loan(connection, loan_details)


def get_business_loan(connection, loan_username, loan_bank_id, loan_amt):
    loan_type = "business"
    total_loan_amt = loan_amt
    loan_balance = loan_amt
    loan_duration = 5
    loan_interest = 12
    loan_details = (loan_bank_id, loan_username, loan_type, total_loan_amt, loan_balance, loan_duration,
                    loan_interest)
    insert_new_loan(connection, loan_details)
