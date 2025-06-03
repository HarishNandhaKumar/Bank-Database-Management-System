import pymysql
from pymysql.cursors import DictCursor


def connect_database():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",  # type your mysql database username
            password="Harish@2171",  # type your mysql database password
            database="bank_db_project",
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connected to the database successfully.")
        return connection
    except pymysql.MySQLError as e:
        print(f"Database connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None
