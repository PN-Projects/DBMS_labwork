import sqlite3
import os

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

def work_on_existing_experiment(cursor):
    print("\nYou selected: Work on Existing Experiment")
    while True:
        try:
            experiment_number = input("Enter the experiment number to work on (or type 'back' to return): ").strip()
            if experiment_number.lower() == "back":
                break
            print_experiment_heading(experiment_number)
            while True:
                sql_query = input(f"Enter SQL query for Experiment {experiment_number} or type 'done' to finish: ")
                if sql_query.lower() == "done":
                    break
                try:
                    cursor.execute(sql_query)
                    connection.commit()
                    print("Query executed successfully.")
                except Exception as e:
                    print("Error executing query:", e)
        except Exception as e:
            print("An error occurred:", e)
            break

def list_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not tables:
        print("No tables available in the database.")
    else:
        print("Available Tables:")
        for table in tables:
            print(f"- {table[0]}")

def display_table(cursor):
    list_tables(cursor)
    table_name = input("\nEnter the name of the table to display: ").strip()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col[1] for col in cursor.fetchall()]

        if not rows:
            print(f"The table '{table_name}' is empty.")
        else:
            # Print table header
            print("\n" + " | ".join(columns))
            print("-" * (len(columns) * 15))
            # Print table rows
            for row in rows:
                print(" | ".join(map(str, row)))
    except Exception as e:
        print(f"Error displaying table '{table_name}':", e)

def insert_values(cursor):
    list_tables(cursor)
    table_name = input("\nSelect the table you want to insert values into: ").strip()
    try:
        # Fetch and display table structure
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col[1] for col in cursor.fetchall()]
        if not columns:
            print(f"Table '{table_name}' does not exist.")
            return
        
        print("\nTable Structure (Column Order):")
        print(" | ".join(columns))
        print("-" * (len(columns) * 15))

        while True:
            user_input = input(f"Enter values for '{table_name}' as comma-separated values or type 'quit' to stop: ")
            if user_input.lower() == "quit":
                break
            try:
                placeholders = ', '.join(['?'] * len(columns))
                insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
                values = tuple(user_input.split(','))
                cursor.execute(insert_query, values)
                connection.commit()
                print(f"Record inserted into '{table_name}' successfully.")
            except Exception as e:
                print("Error inserting record:", e)
    except Exception as e:
        print(f"Error: {e}")

def main_menu(cursor):
    while True:
        print("\nOptions:")
        print("1) Add Experiment")
        print("2) Work on Existing Experiment")
        print("3) Insert Values in DB")
        print("4) Display Tables and Data")
        print("5) Exit")
        choice = input("Select an option (1/2/3/4/5): ").strip()

        if choice == "1":
            experiment_number = input("Enter the experiment number: ")
            add_experiment(cursor, experiment_number)
        elif choice == "2":
            work_on_existing_experiment(cursor)
        elif choice == "3":
            insert_values(cursor)
        elif choice == "4":
            display_table(cursor)
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

try:
    database_file = "local_salespeople_db.sqlite"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    print(f"Connected to the SQLite database: {database_file}")
    main_menu(cursor)
except Exception as e:
    print("An error occurred:", e)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Database connection closed.")
