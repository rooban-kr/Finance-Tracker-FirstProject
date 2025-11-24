import sqlite3

DATABASE_NAME = 'finance_data.db'

# --- 1. SETUP DATABASE FUNCTION (First) ---
def setup_database():
    """Connects to the database and creates the 'transactions' table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

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

# --- 2. ADD TRANSACTION FUNCTION (Second - Must be before it's called) ---
def add_transaction(conn, date, amount, category, transaction_type):
    """Inserts a new transaction record into the database."""
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO transactions (date, amount, category, type)
            VALUES (?, ?, ?, ?)
        """, (date, amount, category, transaction_type))
        
        conn.commit()
        print(f"Transaction added: {transaction_type} of ${amount:.2f} on {date}")

    except sqlite3.Error as e:
        print(f"Error adding transaction: {e}")


# --- 3. MAIN EXECUTION BLOCK (Last) ---
if __name__ == "__main__":
    conn = setup_database()
    if conn:
        print(f"Database '{DATABASE_NAME}' set up successfully.")
        
        # Now Python knows what add_transaction is!
        add_transaction(conn, '2025-11-24', 2500.00, 'Salary', 'Income')
        add_transaction(conn, '2025-11-24', 55.75, 'Groceries', 'Expense')
        
        conn.close()


        