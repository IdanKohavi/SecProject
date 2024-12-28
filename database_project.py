import sqlite3
from prettytable import PrettyTable

def create_database():
    """Create and connects to the database"""
    conn = sqlite3.connect('company.db')
    print("Database connection established")
    return conn

def create_table(conn, table_name, columns):
    """Create a table with the given name and columns"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join([f'{col} {dtype}' for col, dtype in columns.items()])}
                );
            """)
        conn.commit()
        print(f"Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table {table_name}: {e}")

def insert_user(conn, table_name, user_data):
    """Insert user data into the specific table"""
    try:
        cursor = conn.cursor()
        columns = ', '.join(user_data.keys())
        placeholders = ', '.join(['?' for _ in user_data])
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", tuple(user_data.values()))
        conn.commit()
        print(f"User inserted into '{table_name}' successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting user into {table_name}: {e}")

def print_table(conn, table_name):
    """Print all rows from the specified table in a table format"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        if rows:
            cursor.execute(f"PRAGMA table_info('{table_name}')")
            columns_name = [info[1] for info in cursor.fetchall()]
            table = PrettyTable()
            table.field_names = columns_name
            for row in rows:
                table.add_row(row)
            print(f"'\n Contents of table '{table_name}' are:")
            print(table)
        else:
            print(f"Table '{table_name}' is empty.")
    except sqlite3.Error as e:
        print(f"Error reading table '{table_name}': {e}")

def update_password(conn, table_name, user_id, new_password):
    """Update the password for the specified user in the specified table"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN password TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table_name} SET password = '{new_password}' WHERE id = {user_id}")
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Password for user '{user_id}' updated successfully in '{table_name}' table.")
        else:
            print(f"No user with ID '{user_id}' found in '{table_name}' table.")
    except sqlite3.Error as e:
        print(f"Error updating password for user in '{table_name}': {e}")

def main():
    conn = create_database()

    employees_columns = {
        'id': 'INTEGER PRIMARY KEY UNIQUE',
        'first_name': 'TEXT NOT NULL',
        'last_name': 'TEXT NOT NULL',
        'password': 'TEXT',
        'email': 'TEXT NOT NULL UNIQUE',
    }

    clients_columns = {
        'id': 'INTEGER PRIMARY KEY UNIQUE',
        'first_name': 'TEXT NOT NULL',
        'last_name': 'TEXT NOT NULL',
    }

    #create tables
    create_table(conn, 'clients', clients_columns)
    create_table(conn, 'employees', employees_columns)

    #Inserting Users
    employee_data = {
        'id': '123456789',
        'first_name': 'test',
        'last_name': 'test1',
        'password': '11111',
        'email': 'test@gmail.com'
    }

    client_data = {
        'id': '207073314',
        'first_name': 'Idan',
        'last_name': 'Kohavi',
    }

    insert_user(conn, 'clients', client_data)
    insert_user(conn, 'employees', employee_data)

    update_password(conn, 'employees', 207073313, 'New_updated_password')

    #printing tables
    print_table(conn, 'clients')
    print_table(conn, 'employees')

    conn.close()


main()




