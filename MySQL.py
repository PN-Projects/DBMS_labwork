import mysql.connector
from mysql.connector import Error
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def create_local_database():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cursor = connection.cursor()
        local_db_name = "local_salespeople_db"
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {local_db_name};")
        print(f"Local database '{local_db_name}' created or already exists.")
        cursor.close()
        connection.close()
        return mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=local_db_name
        )
    except Error as e:
        print("Error creating or connecting to local database:", e)
        exit()

def print_experiment_heading(number):
    print(f"\n{'='*10} EXPERIMENT {number} {'='*10}")

def add_experiment(cursor, number):
    print_experiment_heading(number)
    while True:
        sql_query = input(f"Enter SQL query for Experiment {number} or type 'done' to finish: ")
        if sql_query.lower() == "done":
            break
        try:
            cursor.execute(sql_query)
            connection.commit()
            print("Query executed successfully.")
        except Exception as e:
            print("Error executing query:", e)

def list_tables(cursor):
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("Available Tables:")
    for table in tables:
        print(f"- {table[0]}")

def insert_values(cursor):
    list_tables(cursor)
    table_name = input("Select the table you want to insert values into: ").strip()
    while True:
        user_input = input(f"Enter values for table '{table_name}' as comma-separated values or type 'quit' to stop: ")
        if user_input.lower() == "quit":
            break
        try:
            cursor.execute(f"DESCRIBE {table_name};")
            columns = [col[0] for col in cursor.fetchall()]
            placeholders = ', '.join(['%s'] * len(columns))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
            values = tuple(user_input.split(','))
            cursor.execute(insert_query, values)
            connection.commit()
            print(f"Record inserted into '{table_name}' successfully.")
        except Exception as e:
            print("Error inserting record:", e)

def main_menu(cursor):
    while True:
        print("\nOptions:")
        print("1) Add Experiment")
        print("2) Insert Values in DB")
        print("3) Exit")
        choice = input("Select an option (1/2/3): ").strip()

        if choice == "1":
            experiment_number = input("Enter the experiment number: ")
            add_experiment(cursor, experiment_number)
        elif choice == "2":
            insert_values(cursor)
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

try:
    if MYSQL_DATABASE:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        print("Connected to the MySQL database successfully!")
    else:
        connection = create_local_database()
        print("Connected to the local MySQL database successfully!")

    cursor = connection.cursor()
    main_menu(cursor)
except Error as e:
    print("An error occurred:", e)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Database connection closed.")
      
