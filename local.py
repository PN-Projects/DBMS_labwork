import sqlite3
import os

def print_heading(title):
    print(f"\n{'='*10} {title} {'='*10}")

def list_tables(cursor):
    """List all tables in the database."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not tables:
        print("No tables available in the database.")
    else:
        print("\nAvailable Tables:")
        for table in tables:
            print(f"- {table[0]}")
    return [table[0] for table in tables]

def display_table(cursor):
    """Display the contents of a selected table."""
    tables = list_tables(cursor)
    if not tables:
        return
    table_name = input("\nEnter the name of the table to display: ").strip()
    if table_name not in tables:
        print(f"Table '{table_name}' does not exist.")
        return
    try:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col[1] for col in cursor.fetchall()]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
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
        print("Error displaying table:", e)

def insert_values(cursor, connection):
    """Insert values into a selected table."""
    tables = list_tables(cursor)
    if not tables:
        return
    table_name = input("\nSelect the table you want to insert values into: ").strip()
    if table_name not in tables:
        print(f"Table '{table_name}' does not exist.")
        return
    try:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col[1] for col in cursor.fetchall()]
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
        print("Error:", e)

def fire_query(cursor, connection):
    """Execute queries from a file or direct input and display the results."""
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
                        try:
                            cursor.execute(query)
                            connection.commit()
                            print(f"Executed: {query}")
                            # If SELECT query, display output
                            if query.lower().startswith("select"):
                                rows = cursor.fetchall()
                                if rows:
                                    print("\nQuery Result:")
                                    for row in rows:
                                        print(row)
                                else:
                                    print("\nQuery executed but returned no results.")
                            else:
                                print("Query executed successfully (Non-SELECT).")
                        except Exception as e:
                            print(f"Error executing query '{query}':", e)
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
                # If SELECT query, display output
                if sql_query.lower().startswith("select"):
                    rows = cursor.fetchall()
                    if rows:
                        print("\nQuery Result:")
                        for row in rows:
                            print(row)
                    else:
                        print("\nQuery executed but returned no results.")
                else:
                    print("Query executed successfully (Non-SELECT).")
            except Exception as e:
                print("Error executing query:", e)
    else:
        print("Invalid option. Please choose 1 or 2.")

def main_menu(cursor, connection):
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
            display_table(cursor)
        elif choice == "3":
            insert_values(cursor, connection)
        elif choice == "4":
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
    main_menu(cursor, connection)
except Exception as e:
    print("An error occurred:", e)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Database connection closed.")
