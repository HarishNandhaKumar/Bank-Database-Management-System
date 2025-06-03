from account import *

from transaction import get_acc_number


def check_valid_ins_choice(prompt_text):
    while True:
        try:
            ins_choice = int(input(prompt_text))
            if 1 <= ins_choice <= 3:
                return int(ins_choice)
            else:
                print("Invalid insurance choice. Please enter a number 1 or 2 or 3.\n")
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")


def check_ins_exists(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT customer_username FROM insurance WHERE customer_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result is not None
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return False


def insert_new_ins(connection, ins_details):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('add_insurance', ins_details)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")


def delete_insurance_username(connection, inv_id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('delete_insurance', (inv_id,))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")


def delete_insurance(connection, username):
    if check_ins_exists(connection, username):
        delete_insurance_username(connection, username)
        print(f"\nINSURANCE DELETED SUCCESSFULLY for USERNAME:{username}\n")
        return
    else:
        print(f"\nNO INSURANCE EXIST for USERNAME:{username}\n"
              f"DELETE OPERATION FAILED\n")
        return


def apply_for_insurance(connection, username):
    ins_username = username
    ins_bank_id = get_user_branch_id(connection, ins_username)
    if check_account_exists(connection, username) is False:
        print("\nNO BANK ACCOUNT FOUND WITH THIS USERNAME.\n"
              "PLEASE CREATE BANK ACCOUNT FIRST AND APPLY FOR INSURANCE\n")
        return

    if check_ins_exists(connection, ins_username):
        print(f"\nUSERNAME {ins_username}, ALREADY HAVE AN INSURANCE!. CANNOT CREATE ANOTHER INSURANCE.\n")
        return

    while True:
        loan_choice = check_valid_ins_choice("\n** Apply for Insurance **\n"
                                             "Choose the type of Insurance:\n"
                                             "1. Life\n"
                                             "2. Health\n"
                                             "3. Auto\n"
                                             "4. Home"
                                             "Your choice: ")
        ins_amt = prompt_for_positive_int("\nEnter the Insurance Coverage amount: (Only Debit Payment)")
        if loan_choice == 1:
            get_life_ins(connection, ins_username, ins_bank_id, ins_amt)
            return
        elif loan_choice == 2:
            get_health_ins(connection, ins_username, ins_bank_id, ins_amt)
            return
        elif loan_choice == 3:
            get_auto_ins(connection, ins_username, ins_bank_id, ins_amt)
            return
        elif loan_choice == 4:
            get_home_ins(connection, ins_username, ins_bank_id, ins_amt)
            return


def get_life_ins(connection, ins_username, ins_bank_id, ins_amt):
    user_acc_number = get_acc_number(connection, ins_username)
    user_acc_balance = get_current_account_balance(connection, (ins_username, user_acc_number))
    if ins_amt > user_acc_number:
        print("\nINSUFFICIENT ACCOUNT BALANCE!.\n"
              "PAYMENT CANCELLED\n")
        return
    new_acc_balance = user_acc_balance - ins_amt
    new_debit_balance = new_acc_balance
    db_card_number = get_debit_card_number(connection, (user_acc_number,))
    update_current_account_balance(connection, user_acc_number, ins_username, new_acc_balance)
    update_debit_card_balance(connection, db_card_number, new_debit_balance)
    t_date = datetime.now().strftime('%Y-%m-%d')
    record_deposit_transaction(connection, user_acc_number, "withdrawal", t_date, ins_amt, "USD",
                               user_acc_balance, new_acc_balance, user_acc_number, "completed")
    insurance_bank_id = ins_bank_id
    ins_type = "life"
    coverage_amt = ins_amt
    ins_term = 20
    ins_status = "active"
    ins_details = (insurance_bank_id, ins_username, ins_type, coverage_amt, ins_term, ins_status)
    insert_new_ins(connection, ins_details)
    print(f"\nLIFE INSURANCE UPDATED for USER {ins_username}\n")


def get_health_ins(connection, ins_username, ins_bank_id, ins_amt):
    user_acc_number = get_acc_number(connection, ins_username)
    user_acc_balance = get_current_account_balance(connection, (ins_username, user_acc_number))
    if ins_amt > user_acc_number:
        print("\nINSUFFICIENT ACCOUNT BALANCE!.\n"
              "PAYMENT CANCELLED\n")
        return
    new_acc_balance = user_acc_balance - ins_amt
    new_debit_balance = new_acc_balance
    db_card_number = get_debit_card_number(connection, (user_acc_number,))
    update_current_account_balance(connection, user_acc_number, ins_username, new_acc_balance)
    update_debit_card_balance(connection, db_card_number, new_debit_balance)
    t_date = datetime.now().strftime('%Y-%m-%d')
    record_deposit_transaction(connection, user_acc_number, "withdrawal", t_date, ins_amt, "USD",
                               user_acc_balance, new_acc_balance, user_acc_number, "completed")
    insurance_bank_id = ins_bank_id
    ins_type = "health"
    coverage_amt = ins_amt
    ins_term = 10
    ins_status = "active"
    ins_details = (insurance_bank_id, ins_username, ins_type, coverage_amt, ins_term, ins_status)
    insert_new_ins(connection, ins_details)
    print(f"\nHEALTH INSURANCE UPDATED for USER {ins_username}\n")


def get_auto_ins(connection, ins_username, ins_bank_id, ins_amt):
    user_acc_number = get_acc_number(connection, ins_username)
    user_acc_balance = get_current_account_balance(connection, (ins_username, user_acc_number))
    if ins_amt > user_acc_number:
        print("\nINSUFFICIENT ACCOUNT BALANCE!.\n"
              "PAYMENT CANCELLED\n")
        return
    new_acc_balance = user_acc_balance - ins_amt
    new_debit_balance = new_acc_balance
    db_card_number = get_debit_card_number(connection, (user_acc_number,))
    update_current_account_balance(connection, user_acc_number, ins_username, new_acc_balance)
    update_debit_card_balance(connection, db_card_number, new_debit_balance)
    t_date = datetime.now().strftime('%Y-%m-%d')
    record_deposit_transaction(connection, user_acc_number, "withdrawal", t_date, ins_amt, "USD",
                               user_acc_balance, new_acc_balance, user_acc_number, "completed")
    insurance_bank_id = ins_bank_id
    ins_type = "auto"
    coverage_amt = ins_amt
    ins_term = 5
    ins_status = "active"
    ins_details = (insurance_bank_id, ins_username, ins_type, coverage_amt, ins_term, ins_status)
    insert_new_ins(connection, ins_details)
    print(f"\nAUTO INSURANCE UPDATED for USER {ins_username}\n")


def get_home_ins(connection, ins_username, ins_bank_id, ins_amt):
    user_acc_number = get_acc_number(connection, ins_username)
    user_acc_balance = get_current_account_balance(connection, (ins_username, user_acc_number))
    if ins_amt > user_acc_number:
        print("\nINSUFFICIENT ACCOUNT BALANCE!.\n"
              "PAYMENT CANCELLED\n")
        return
    new_acc_balance = user_acc_balance - ins_amt
    new_debit_balance = new_acc_balance
    db_card_number = get_debit_card_number(connection, (user_acc_number,))
    update_current_account_balance(connection, user_acc_number, ins_username, new_acc_balance)
    update_debit_card_balance(connection, db_card_number, new_debit_balance)
    t_date = datetime.now().strftime('%Y-%m-%d')
    record_deposit_transaction(connection, user_acc_number, "withdrawal", t_date, ins_amt, "USD",
                               user_acc_balance, new_acc_balance, user_acc_number, "completed")
    insurance_bank_id = ins_bank_id
    ins_type = "home"
    coverage_amt = ins_amt
    ins_term = 15
    ins_status = "active"
    ins_details = (insurance_bank_id, ins_username, ins_type, coverage_amt, ins_term, ins_status)
    insert_new_ins(connection, ins_details)
    print(f"\nHOME INSURANCE UPDATED for USER {ins_username}\n")
