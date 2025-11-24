import sqlite3

DATABASE_NAME = 'finance_data.db'

def setup_database():
    """Connects to the database and creates the 'transactions' table if it doesn't exist."""
    try:
        # Connect to the database file (creates it if it doesn't exist)
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Define the schema (what data fields each transaction will have)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                type TEXT NOT NULL  -- 'Income' or 'Expense'
            )
        """)
        
        conn.commit()
        return conn

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

if __name__ == "__main__":
    conn = setup_database()
    if conn:
        print(f"Database '{DATABASE_NAME}' set up successfully.")
        conn.close()