import sqlite3
import os
from datetime import datetime

# Function to print experiment headings
def print_experiment_heading(number):
    print(f"\n{'='*10} EXPERIMENT {number} {'='*10}")

# Initialize the experiments table
def initialize_experiment_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            experiment_number TEXT,
            query TEXT,
            executed_at TEXT
        );
    """)
    connection.commit()

# Add a new experiment
def add_experiment(cursor, number):
    print_experiment_heading(number)
    while True:
        sql_query = input(f"Enter SQL query for Experiment {number} or type 'done' to finish: ")
        if sql_query.lower() == "done":
            break
        try:
            cursor.execute(sql_query)
            connection.commit()
            # Store the query in the experiments table
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO experiments (experiment_number, query, executed_at) VALUES (?, ?, ?)",
                (number, sql_query, timestamp)
            )
            connection.commit()
            print("Query executed and saved successfully.")
        except Exception as e:
            print("Error executing query:", e)

# List all existing experiments
def list_existing_experiments(cursor):
    cursor.execute("SELECT DISTINCT experiment_number FROM experiments")
    experiments = cursor.fetchall()
    if not experiments:
        print("No experiments found.")
        return []
    print("\nExisting Experiments:")
    for exp in experiments:
        print(f"- Experiment {exp[0]}")
    return [exp[0] for exp in experiments]

# Work on an existing experiment
def work_on_existing_experiment(cursor):
    print("\nYou selected: Work on Existing Experiment")
    existing_experiments = list_existing_experiments(cursor)
    if not existing_experiments:
        return
    experiment_number = input("Enter the experiment number to work on: ").strip()
    if experiment_number not in existing_experiments:
        print(f"Experiment {experiment_number} does not exist.")
        return

    print_experiment_heading(experiment_number)
    # Display previous queries
    cursor.execute("SELECT query, executed_at FROM experiments WHERE experiment_number = ?", (experiment_number,))
    queries = cursor.fetchall()
    print("\nPrevious Queries:")
    for query, executed_at in queries:
        print(f"[{executed_at}] {query}")

    # Allow user to add new queries
    while True:
        sql_query = input(f"Enter SQL query for Experiment {experiment_number} or type 'done' to finish: ")
        if sql_query.lower() == "done":
            break
        try:
            cursor.execute(sql_query)
            connection.commit()
            # Store the query
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO experiments (experiment_number, query, executed_at) VALUES (?, ?, ?)",
                (experiment_number, sql_query, timestamp)
            )
            connection.commit()
            print("Query executed and saved successfully.")
        except Exception as e:
            print("Error executing query:", e)

# List all tables
def list_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not tables:
        print("No tables available in the database.")
    else:
        print("Available Tables:")
        for table in tables:
            print(f"- {table[0]}")

# Display the contents of a table
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
            print("\n" + " | ".join(columns))
            print("-" * (len(columns) * 15))
            for row in rows:
                print(" | ".join(map(str, row)))
    except Exception as e:
        print(f"Error displaying table '{table_name}':", e)

# Insert values into a table
def insert_values(cursor):
    list_tables(cursor)
    table_name = input("\nSelect the table you want to insert values into: ").strip()
    try:
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

# Main menu
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

# Program execution
try:
    database_file = "local_salespeople_db.sqlite"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    print(f"Connected to the SQLite database: {database_file}")
    initialize_experiment_table(cursor)
    main_menu(cursor)
except Exception as e:
    print("An error occurred:", e)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Database connection closed.")
