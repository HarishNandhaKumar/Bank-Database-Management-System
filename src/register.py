import pymysql
from datetime import datetime


def prompt_for_int(prompt_text):
    while True:
        try:
            return int(input(prompt_text))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def prompt_for_date(prompt_text):
    while True:
        date_input = input(prompt_text)
        try:
            return datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")


def prompt_for_gender(prompt_text):
    while True:
        gender = input(prompt_text).strip().lower()
        if gender in {"male", "female", "other"}:
            return gender
        else:
            print("Invalid input. Please try again.")


def prompt_for_phone_number(prompt_text):
    while True:
        user_input = input(prompt_text).strip()
        if user_input.isdigit() and len(user_input) == 10:
            return user_input
        else:
            print("Invalid Phone Number. Please enter exactly 10 digits.")


def prompt_for_ssn(prompt_text):
    while True:
        user_input = input(prompt_text).strip()
        if user_input.isdigit() and len(user_input) == 9:
            return user_input
        else:
            print("Invalid SSN number. Please enter exactly 9 digits.")


def prompt_for_zipcode(prompt_text):
    while True:
        user_input = input(prompt_text).strip()
        if user_input.isdigit() and len(user_input) == 5:
            return user_input
        else:
            print("Invalid Zipcode. Please enter exactly 5 digits.")


def check_branch_id(prompt_text):
    while True:
        try:
            branch_choice = int(input(prompt_text))
            if 1 <= branch_choice <= 4:
                return int(branch_choice)
            else:
                print("Invalid choice. Please enter a number between 1 and 4.\n")
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")


def get_address_id(connection, user_address):
    try:
        with connection.cursor() as cursor:

            user_address_with_out = user_address + (0,)
            cursor.callproc('get_user_address_id', user_address_with_out)
            cursor.execute("SELECT @_get_user_address_id_6")
            result = cursor.fetchone()
            return int(result['@_get_user_address_id_6'])

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None


def check_username(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT c_username FROM customer WHERE c_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result is not None  # True if username exists
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return False


def register_user_details(connection, user_data):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('register_user_details', user_data)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")


def register_user_address(connection, user_address):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('register_user_address', user_address)
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")


def insert_user_address_id(connection, user_address_id, username):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('insert_customer_address_id', (user_address_id, username))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")


def SignUp(connection):
    username = input("Enter your username: ")
    if check_username(connection, username):
        print("Username exists. Please Sign In!")
    else:
        branch_id = check_branch_id("\nEnter your preferred bank branch option from the following:\n"
                                    "1. Downtown branch\n"
                                    "2. Uptown branch\n"
                                    "3. Northside\n"
                                    "4. Eastside\n"
                                    "Your choice number:")

        print("\nEnter your details:\n")
        user_data = (
            username,
            input("Enter password: "),
            input("Enter first name: ").lower(),
            input("Enter last name: ").lower(),
            prompt_for_int("Enter age: "),
            prompt_for_date("Enter date of birth (YYYY-MM-DD): "),
            prompt_for_gender("Enter gender: ('male', 'female', or 'other') "),
            prompt_for_phone_number("Enter phone number (10 digits): "),
            prompt_for_ssn("Enter SSN: "),
            branch_id
        )

        print("\nEnter your Address details:\n")
        user_address = (
            prompt_for_int("Enter the street number: "),
            input("Enter the street name: ").lower(),
            input("Enter the town name: ").lower(),
            input("Enter the city name: ").lower(),
            input("Enter the state name: ").lower(),
            prompt_for_zipcode("Enter the zip code: ")
        )

        register_user_details(connection, user_data)
        register_user_address(connection, user_address)
        user_address_id = get_address_id(connection, user_address)
        insert_user_address_id(connection, user_address_id, username)

        print("REGISTERED SUCCESSFULLY, SIGN IN NOW!")
        return username


def SignIn(connection):
    while True:
        temp = None
        username = input("Enter Username to Sign In: (Enter 'Q' to quit)\n=> ")
        if username == 'Q':
            return username
        query = "SELECT c_password FROM customer WHERE c_username = %s"
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (username,))
                temp = cursor.fetchone()
        except Exception as e:
            print(f"Username does not exist. Please SignUp!")
            SignUp(connection)

        if temp:
            while True:
                password = input("Enter Password: ")
                if list(temp.values())[0] == password:
                    print("Sign IN Successfully")
                    return username
                else:
                    print("Wrong Password, Try Again.")
        else:
            print("Invalid Username. Please try again.")
