import psycopg2
from psycopg2 import sql
import os
from config import POSTGRESQL_DATABASE_URI as DATABASE_URI

def create_local_database():
    print("No database URI provided. Setting up a local database...")
    try:
        connection = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
        connection.autocommit = True
        cursor = connection.cursor()

        local_db_name = "local_salespeople_db"
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{local_db_name}';")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {local_db_name};")
            print(f"Local database '{local_db_name}' created successfully.")
        else:
            print(f"Local database '{local_db_name}' already exists.")

        cursor.close()
        connection.close()

        # Connect to the local database
        local_connection = psycopg2.connect(
            dbname=local_db_name, user="postgres", password="postgres", host="localhost"
        )
        return local_connection
    except Exception as e:
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
            if cursor.description:
                print("Result:", cursor.fetchall())
            else:
                print("Query executed successfully.")
        except Exception as e:
            print("Error executing query:", e)

def list_tables(cursor):
    cursor.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public';
    """)
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
            columns_query = f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{table_name}';
            """
            cursor.execute(columns_query)
            columns = [col[0] for col in cursor.fetchall()]
            placeholders = ', '.join(['%s'] * len(columns))
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            values = tuple(user_input.split(','))
            cursor.execute(insert_query, values)
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
            connection.commit()
        elif choice == "2":
            insert_values(cursor)
            connection.commit()
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

try:
    if DATABASE_URI:
        connection = psycopg2.connect(DATABASE_URI)
        print("Connected to the remote database successfully!")
    else:
        connection = create_local_database()
        print("Connected to the local database successfully!")

    cursor = connection.cursor()
    main_menu(cursor)

except Exception as e:
    print("An error occurred:", e)
    if connection:
        connection.rollback()
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Database connection closed.")
              
