import pymysql
from tabulate import tabulate

from transaction import get_acc_number


def check_valid_dsp_choice(prompt_text):
    try:
        dsp_choice = int(input(prompt_text))
        if 1 <= dsp_choice <= 7:
            return dsp_choice
        else:
            print("Invalid Display choice. Please enter a number between 0 and 7.\n")
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")


def display_details(connection, username):
    while True:
        dsp_choice = check_valid_dsp_choice("\n** Display User Details **\n"
                                            "Choose the option to display that details:\n"
                                            "1. Customer Details\n"
                                            "2. Account Details\n"
                                            "3. Card Details\n"
                                            "4. Loan Details\n"
                                            "5. Investment Details\n"
                                            "6. Insurance Details\n"
                                            "7. Transaction Details\n"
                                            "Your choice: ")
        if dsp_choice == 1:
            customer_details(connection, username)
            return
        elif dsp_choice == 2:
            account_details(connection, username)
            return
        elif dsp_choice == 3:
            card_details(connection, username)
            return
        elif dsp_choice == 4:
            loan_details(connection, username)
            return
        elif dsp_choice == 5:
            investment_details(connection, username)
            return
        elif dsp_choice == 6:
            insurance_details(connection, username)
            return
        elif dsp_choice == 7:
            transaction_details(connection, username)
            return


def customer_details(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM customer WHERE c_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchall()
            if result:
                print(tabulate(result, headers="keys", tablefmt="fancy_grid", numalign="center"))
            else:
                print("No records found.")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None


def account_details(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM bank_account WHERE acc_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchall()
            if result:
                print(tabulate(result, headers="keys", tablefmt="fancy_grid", numalign="center"))
            else:
                print("No records found.")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None


def card_details(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM card WHERE card_holder_name = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchall()
            if result:
                print(tabulate(result, headers="keys", tablefmt="fancy_grid", numalign="center"))
            else:
                print("No records found.")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None


def loan_details(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM loan WHERE customer_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchall()
            if result:
                print(tabulate(result, headers="keys", tablefmt="fancy_grid", numalign="center"))
            else:
                print("No records found.")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None


def investment_details(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM investment WHERE customer_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchall()
            if result:
                print(tabulate(result, headers="keys", tablefmt="fancy_grid", numalign="center"))
            else:
                print("No records found.")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None


def insurance_details(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM insurance WHERE customer_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchall()
            if result:
                print(tabulate(result, headers="keys", tablefmt="fancy_grid", numalign="center"))
            else:
                print("No records found.")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None


def transaction_details(connection, username):
    try:
        user_acc_num = get_acc_number(connection, username)
        with connection.cursor() as cursor:
            query = "SELECT * FROM transactions WHERE t_acc_number = %s"
            cursor.execute(query, (user_acc_num,))
            result = cursor.fetchall()
            if result:
                print(tabulate(result, headers="keys", tablefmt="fancy_grid", numalign="center"))
            else:
                print("No records found.")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None