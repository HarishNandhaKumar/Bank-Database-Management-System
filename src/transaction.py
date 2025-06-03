from account import *


def get_acc_number(connection, username):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('get_account_number', (username, None))
            cursor.execute("SELECT @_get_account_number_1")
            result = cursor.fetchone()
            if result['@_get_account_number_1'] is None:
                return
            return int(result['@_get_account_number_1'])

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None


def check_valid_payment_choice(prompt_text):
    while True:
        try:
            payment_choice = int(input(prompt_text))
            if 1 <= payment_choice <= 2:
                return int(payment_choice)
            else:
                print("Invalid payment choice. Please enter a number 1 or 2.\n")
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")


def get_receiver_acc_number(connection, sender_acc_num, prompt_text):
    while True:
        try:
            receiver_acc_num = int(input(prompt_text))
            if check_acc_num_exists(connection, receiver_acc_num) and (receiver_acc_num != sender_acc_num):
                return receiver_acc_num
            else:
                print("Receiver account number does not exist. Please check the number you've entered.\n")
        except ValueError:
            print("Invalid input. Please enter a valid account number.\n")


def get_username(connection, acc_num):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('get_username_from_bank_account', (acc_num, None))
            cursor.execute("SELECT @_get_username_from_bank_account_1")
            result = cursor.fetchone()
            return result['@_get_username_from_bank_account_1']

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None


def check_acc_num_exists(connection, receiver_acc_num):
    try:
        with connection.cursor() as cursor:
            query = "SELECT acc_number FROM bank_account WHERE acc_number = %s"
            cursor.execute(query, (receiver_acc_num,))
            result = cursor.fetchone()
            return result is not None
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return False


def get_credit_card_num(connection, sender_acc_details):
    try:
        with connection.cursor() as cursor:
            user_acc_details = sender_acc_details + (0,)
            cursor.callproc('get_credit_card_number', user_acc_details)
            cursor.execute("SELECT @_get_credit_card_number_1")
            result = cursor.fetchone()
            return int(result['@_get_credit_card_number_1'])

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None


def get_credit_card_limit(connection, credit_card_num):
    try:
        with connection.cursor() as cursor:
            user_ccc_number = credit_card_num + (0,)
            cursor.callproc('get_credit_card_limit', user_ccc_number)
            cursor.execute("SELECT @_get_credit_card_limit_1")
            result = cursor.fetchone()
            return int(result['@_get_credit_card_limit_1'])
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None


def get_credit_available(connection, credit_card_num):
    try:
        with connection.cursor() as cursor:
            user_ccc_number = credit_card_num + (0,)
            cursor.callproc('get_credit_card_available_credit', user_ccc_number)
            cursor.execute("SELECT @_get_credit_card_available_credit_1")
            result = cursor.fetchone()
            return int(result['@_get_credit_card_available_credit_1'])
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None


def get_used_credit(connection, credit_card_num):
    try:
        with connection.cursor() as cursor:
            user_ccc_number = credit_card_num + (0,)
            cursor.callproc('get_credit_card_credit_used', user_ccc_number)
            cursor.execute("SELECT @_get_credit_card_credit_used_1")
            result = cursor.fetchone()
            return int(result['@_get_credit_card_credit_used_1'])
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None


def update_credit_card_balances(connection, cc_card_number, cc_credit_used, cc_available_credit):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('update_credit_card_balances', (cc_card_number, cc_credit_used, cc_available_credit))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")


def record_account_transaction(connection, acc_number, t_type, t_date, t_amount, t_cur_type, t_before_balance,
                               t_balance_after, sender_acc_id, receiver_acc_id, t_status):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('record_account_transaction',
                            (acc_number, t_type, t_date, t_amount, t_cur_type, t_before_balance, t_balance_after,
                             sender_acc_id, receiver_acc_id, t_status))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")


def transaction(connection, username):
    sender_username = username
    if check_account_exists(connection, username) is False:
        print("\nNO BANK ACCOUNT FOUND WITH THIS USERNAME. CANNOT MAKE TRANSACTIONS\n")
        return

    while True:
        payment_method = check_valid_payment_choice("\n** Transfer amount to other account **"
                                                    "Enter your choice for payment method:\n"
                                                    "1. Debit Card payment\n"
                                                    "2. Credit Card payment\n"
                                                    "Your choice: ")
        if payment_method == 1:
            debit_card_payment(connection, sender_username)
            return
        elif payment_method == 2:
            credit_card_payment(connection, sender_username)
            return


def debit_card_payment(connection, sender_username):
    print("\nENTER THE DETAILS FOR DEBIT CARD TRANSACTION\n")
    sender_acc_number = get_acc_number(connection, sender_username)
    sender_cur_bal = get_current_account_balance(connection, (sender_username, sender_acc_number))
    amount_to_send = prompt_for_positive_int("\nEnter the amount to send: ")
    if sender_cur_bal < amount_to_send:
        print(f"INSUFFICIENT BALANCE! Your current balance: {sender_cur_bal}\n"
              f"TRANSACTION FAILED\n")
        return

    receiver_acc_number = prompt_for_valid_acc_number("\nEnter the receiver account number: ")
    if check_acc_num_exists(connection, receiver_acc_number) is False:
        print(f"RECEIVER ACCOUNT NUMBER: {receiver_acc_number} cannot be found\n"
              f"TRANSACTION FAILED\n")
        return
    elif sender_acc_number == receiver_acc_number:
        print(f"YOU ENTERED YOUR OWN ACCOUNT NUMBER. ENTER ANOTHER ACCOUNT NUMBER.\n"
              f"TRANSACTION FAILED\n")
        return

    receiver_username = get_username(connection, receiver_acc_number)
    receiver_cur_bal = get_current_account_balance(connection, (receiver_username, receiver_acc_number))

    receiver_new_bal = receiver_cur_bal + amount_to_send
    sender_new_bal = sender_cur_bal - amount_to_send

    if sender_new_bal < 0:
        sender_new_bal = 0

    # updated the newly calculated balances in both accounts.
    update_current_account_balance(connection, sender_acc_number, sender_username, sender_new_bal)
    update_current_account_balance(connection, receiver_acc_number, receiver_username, receiver_new_bal)

    transaction_timestamp = datetime.now().strftime('%Y-%m-%d')

    # updating the debit balances for both accounts.
    sender_db_card_num = get_debit_card_number(connection, (sender_acc_number,))
    receiver_db_card_num = get_debit_card_number(connection, (receiver_acc_number,))
    update_debit_card_balance(connection, sender_db_card_num, sender_new_bal)
    update_debit_card_balance(connection, receiver_db_card_num, receiver_new_bal)

    record_account_transaction(connection, sender_acc_number, "transfer", transaction_timestamp, amount_to_send,
                               "USD", sender_cur_bal, sender_new_bal, sender_acc_number, receiver_acc_number,
                               "completed")
    record_account_transaction(connection, receiver_acc_number, "transfer", transaction_timestamp, amount_to_send,
                               "USD", receiver_cur_bal, receiver_new_bal, sender_acc_number, receiver_acc_number,
                               "completed")

    print(f"\nAMOUNT TRANSFERRED SUCCESSFULLY.\n"
          f"***********************\n"
          f"TRANSACTION SUMMARY: \n"
          f"***********************\n"
          f"sender account number: {sender_acc_number}\n"
          f"sender old balance: {sender_cur_bal}\n"
          f"sender new balance: {sender_new_bal}\n"
          f"******\n"
          f"amount transferred: {amount_to_send}\n"
          f"transaction time: {transaction_timestamp}\n"
          f"******\n"
          f"receiver account number: {receiver_acc_number}\n"
          f"receiver old balance: {receiver_cur_bal}\n"
          f"receiver new balance: {receiver_new_bal}\n"
          f"************************\n")

    return


def credit_card_payment(connection, sender_username):
    print("\nENTER THE DETAILS FOR CREDIT CARD TRANSACTION\n")
    sender_acc_number = get_acc_number(connection, sender_username)
    get_current_account_balance(connection, (sender_username, sender_acc_number))

    sender_credit_card_num = get_credit_card_num(connection, (sender_acc_number,))
    get_credit_card_limit(connection, (sender_credit_card_num,))
    cc_available_credit = get_credit_available(connection, (sender_credit_card_num,))
    cc_used_credit = get_used_credit(connection, (sender_credit_card_num,))

    amount_to_send = prompt_for_positive_int("\nEnter the amount to send: ")
    if amount_to_send > cc_available_credit:
        print("INSUFFICIENT AVAILABLE CREDIT IN YOUR CREDIT CARD\n"
              "TRANSACTION FAILED!\n")
        return

    receiver_acc_number = prompt_for_valid_acc_number("\nEnter the receiver account number: ")
    if check_acc_num_exists(connection, receiver_acc_number) is False:
        print(f"RECEIVER ACCOUNT NUMBER: {receiver_acc_number} cannot be found\n"
              f"TRANSACTION FAILED\n")
        return
    elif sender_acc_number == receiver_acc_number:
        print(f"YOU ENTERED YOUR OWN ACCOUNT NUMBER. ENTER ANOTHER ACCOUNT NUMBER.\n"
              f"TRANSACTION FAILED\n")
        return

    receiver_username = get_username(connection, receiver_acc_number)
    receiver_cur_bal = get_current_account_balance(connection, (receiver_username, receiver_acc_number))

    receiver_new_bal = receiver_cur_bal + amount_to_send
    sender_new_available_credit = cc_available_credit - amount_to_send
    sender_new_credit_used = cc_used_credit + amount_to_send

    if sender_new_available_credit < 0:
        sender_new_available_credit = 0

    # updated the newly calculated balances in receiver account
    update_current_account_balance(connection, receiver_acc_number, receiver_username, receiver_new_bal)

    transaction_timestamp = datetime.now().strftime('%Y-%m-%d')

    # updating the debit balance for receiver account.
    receiver_db_card_num = get_debit_card_number(connection, (receiver_acc_number,))
    update_debit_card_balance(connection, receiver_db_card_num, receiver_new_bal)

    # updating the sender's credit card details
    update_credit_card_balances(connection, sender_credit_card_num, sender_new_credit_used,
                                sender_new_available_credit)

    record_account_transaction(connection, sender_acc_number, "credit", transaction_timestamp, amount_to_send,
                               "USD", cc_available_credit, sender_new_available_credit, sender_acc_number,
                               receiver_acc_number, "completed")
    record_account_transaction(connection, receiver_acc_number, "transfer", transaction_timestamp, amount_to_send,
                               "USD", receiver_cur_bal, receiver_new_bal, sender_acc_number, receiver_acc_number,
                               "completed")

    print(f"\nAMOUNT TRANSFERRED SUCCESSFULLY.\n"
          f"***********************\n"
          f"TRANSACTION SUMMARY: \n"
          f"***********************\n"
          f"sender account number: {sender_acc_number}\n"
          f"sender credit card number: {sender_credit_card_num}\n"
          f"sender old credit card balance: {cc_available_credit}\n"
          f"sender new credit card balance: {sender_new_available_credit}\n"
          f"******\n"
          f"amount transferred: {amount_to_send}\n"
          f"transaction time: {transaction_timestamp}\n"
          f"******\n"
          f"receiver account number: {receiver_acc_number}\n"
          f"receiver old balance: {receiver_cur_bal}\n"
          f"receiver new balance: {receiver_new_bal}\n"
          f"************************\n")

    return
