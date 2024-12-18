import os
import sqlite3
import psycopg2
import mysql.connector
from config import DATABASE_URI

def print_heading(title):
    print(f"\n{'='*10} {title} {'='*10}")

def get_database_connection():
    """Connect to the appropriate database based on the DATABASE_URI."""
    if DATABASE_URI.startswith("postgresql://"):
        try:
            print("Connecting to PostgreSQL...")
            connection = psycopg2.connect(DATABASE_URI)
            return connection, "PostgreSQL"
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
    elif DATABASE_URI.startswith("mysql://"):
        try:
            print("Connecting to MySQL...")
            uri_parts = DATABASE_URI.replace("mysql://", "").split(":")
            user, password_host = uri_parts[0], uri_parts[1]
            password, host_db = password_host.split("@")
            host, dbname = host_db.split("/")
            connection = mysql.connector.connect(
                user=user,
                password=password,
                host=host,
                database=dbname
            )
            return connection, "MySQL"
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")
    else:
        # Default to SQLite3
        print("No DATABASE_URI provided. Connecting to local SQLite3 database...")
        connection = sqlite3.connect("local_db.sqlite")
        return connection, "SQLite3"

def list_tables(cursor, db_type):
    """List tables in the database."""
    if db_type == "PostgreSQL":
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    elif db_type == "MySQL":
        cursor.execute("SHOW TABLES;")
    elif db_type == "SQLite3":
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not tables:
        print("No tables available in the database.")
    else:
        print("\nAvailable Tables:")
        for table in tables:
            print(f"- {table[0]}")
    return [table[0] for table in tables]

def display_table(cursor, db_type):
    """Display the contents of a selected table."""
    tables = list_tables(cursor, db_type)
    if not tables:
        return
    table_name = input("\nEnter the name of the table to display: ").strip()
    if table_name not in tables:
        print(f"Table '{table_name}' does not exist.")
        return
    try:
        if db_type == "SQLite3":
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [col[1] for col in cursor.fetchall()]
        elif db_type == "PostgreSQL":
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s;", (table_name,))
            columns = [col[0] for col in cursor.fetchall()]
        elif db_type == "MySQL":
            cursor.execute(f"DESCRIBE {table_name};")
            columns = [col[0] for col in cursor.fetchall()]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        if not rows:
            print(f"The table '{table_name}' is empty.")
        else:
            print("\n" + " | ".join(columns))
            print("-" * (len(columns) * 15))
            for row in rows:
                print(" | ".join(map(str, row)))
    except Exception as e:
        print("Error displaying table:", e)

def insert_values(cursor, connection, db_type):
    """Insert values into a selected table."""
    tables = list_tables(cursor, db_type)
    if not tables:
        return
    table_name = input("\nSelect the table you want to insert values into: ").strip()
    if table_name not in tables:
        print(f"Table '{table_name}' does not exist.")
        return
    try:
        if db_type == "SQLite3":
            cursor.execute(f"PRAGMA table_info({table_name});")
        elif db_type == "PostgreSQL":
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s;", (table_name,))
        elif db_type == "MySQL":
            cursor.execute(f"DESCRIBE {table_name};")
        columns = [col[1] if db_type == "SQLite3" else col[0] for col in cursor.fetchall()]
        print("\nTable Structure (Column Order):")
        print(" | ".join(columns))
        print("-" * (len(columns) * 15))

        while True:
            user_input = input(f"Enter values for '{table_name}' as comma-separated values or type 'quit' to stop: ")
            if user_input.lower() == "quit":
                break
            try:
                placeholders = ', '.join(['%s'] * len(columns)) if db_type != "SQLite3" else ', '.join(['?'] * len(columns))
                insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                values = tuple(user_input.split(','))
                cursor.execute(insert_query, values)
                connection.commit()
                print(f"Record inserted into '{table_name}' successfully.")
            except Exception as e:
                print("Error inserting record:", e)
    except Exception as e:
        print("Error:", e)

def fire_query(cursor, connection):
    """Execute queries from a file or direct input."""
    print_heading("FIRE QUERY")
    print("1) Fire queries from a text file")
    print("2) Fire queries from direct input")
    option = input("Choose an option (1/2): ").strip()
    if option == "1":
        file_path = input("Enter the path or name of the text file: ").strip()
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    queries = file.read()
                for query in queries.split(";"):
                    query = query.strip()
                    if query:
                        cursor.execute(query)
                        print(f"Executed: {query}")
                connection.commit()
                print("All queries executed successfully.")
            except Exception as e:
                print("Error executing queries from file:", e)
        else:
            print("File not found. Please check the path or name.")
    elif option == "2":
        while True:
            sql_query = input("Enter SQL query (or type 'done' to finish): ").strip()
            if sql_query.lower() == "done":
                break
            try:
                cursor.execute(sql_query)
                connection.commit()
                print("Query executed successfully.")
            except Exception as e:
                print("Error executing query:", e)
    else:
        print("Invalid option. Please choose 1 or 2.")

def main_menu(cursor, connection, db_type):
    """Main menu for user interaction."""
    while True:
        print("\nOptions:")
        print("1) Fire Query")
        print("2) Display Tables and Data")
        print("3) Insert Values in DB")
        print("4) Exit")
        choice = input("Select an option (1/2/3/4): ").strip()

        if choice == "1":
            fire_query(cursor, connection)
        elif choice == "2":
            display_table(cursor, db_type)
        elif choice == "3":
            insert_values(cursor, connection, db_type)
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

# Program Execution
try:
    connection, db_type = get_database_connection()
    cursor = connection.cursor()
    print(f"Connected to {db_type} database successfully.")
    main_menu(cursor, connection, db_type)
except Exception as e:
    print("An error occurred:", e)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Database connection closed.")
