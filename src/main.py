from database import *
from display import *
from insurance import apply_for_insurance, delete_insurance
from investment import make_investment, delete_investment
from loan import *


def main_menu(connection, username):
    while True:
        try:
            print(f"USERNAME ACTIVE: {username}\n")
            choice = int(input("\n*** Welcome to Main Menu ***\n"
                               "1. Create Bank Account (generates debit and credit card too)\n"
                               "2. Deposit Amount to your Account\n"
                               "3. Transfer Amount to Another Account\n"
                               "4. Apply Loan\n"
                               "5. Pay Your Loan\n"
                               "6. Make Investment\n"
                               "7. Delete Investment\n"
                               "8. Take an Insurance Policy\n"
                               "9. Delete Insurance\n"
                               "10. Display User Details\n"
                               "11. SignOut\n"
                               "Enter your Option:\n=> "))
            if choice == 1:
                create_account(connection, username)
                return
            elif choice == 2:
                deposit_amount(connection, username)
                return
            elif choice == 3:
                transaction(connection, username)
                return
            elif choice == 4:
                apply_loan(connection, username)
                return
            elif choice == 5:
                pay_loan(connection, username)
                return
            elif choice == 6:
                make_investment(connection, username)
                return
            elif choice == 7:
                delete_investment(connection, username)
                return
            elif choice == 8:
                apply_for_insurance(connection, username)
                return
            elif choice == 9:
                delete_insurance(connection, username)
                return
            elif choice == 10:
                display_details(connection, username)
                return
            elif choice == 11:
                print("\nGet back to SignIn page\n")
                return
            else:
                print("Please Enter Valid Input From Options")

        except ValueError:
            print("Invalid Input Try Again with Numbers")


def main():
    connection = None
    while connection is None:
        connection = connect_database()
        if not connection:
            print("Failed to connect to the database. Please try again.")

    username = None
    while True:
        try:
            choice = int(input("\nWelcome to Boston Bank\n"
                               "1. SignUp\n"
                               "2. SignIn\n"
                               "3. Quit\n"
                               "Enter your Option:\n=> "))
            if choice == 1:
                username = SignUp(connection)
            elif choice == 2:
                username = SignIn(connection)
                if username == 'Q':
                    continue
                else:
                    main_menu(connection, username)
            elif choice == 3:
                print("Thank you for using our App!")
                break
            else:
                print("Please Enter Valid Input From Options")

        except ValueError:
            print("Invalid Input Try Again with Numbers")


if __name__ == "__main__":
    main()
