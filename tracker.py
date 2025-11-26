import sqlite3

DATABASE_NAME = 'finance_data.db'

# --- 1. SETUP DATABASE FUNCTION (First) ---
def setup_database():
    """Connects to the database and creates the 'transactions' table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        # IMPORTANT: Allows accessing columns by name instead of index (needed for Streamlit's data handling)
        conn.row_factory = sqlite3.Row 
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

# --- 2. CREATE FUNCTION ---
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

# --- 3. READ FUNCTION (FOR TERMINAL) ---
def view_transactions(conn):
    """Retrieves and displays all transactions from the database (for terminal use)."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, amount, category, type FROM transactions ORDER BY date DESC")
        transactions = cursor.fetchall()
        
        if not transactions:
            print("\nNo transactions found.")
            return

        print("\n--- TRANSACTION HISTORY ---")
        print(f"{'ID':<4} | {'Date':<10} | {'Type':<8} | {'Category':<15} | {'Amount':>10}")
        print("-" * 50)
        
        for tx in transactions:
            tx_id, date, amount, category, tx_type = tx
            amount_str = f"${amount:,.2f}"
            print(f"{tx_id:<4} | {date:<10} | {tx_type:<8} | {category:<15} | {amount_str:>10}")

    except sqlite3.Error as e:
        print(f"Error viewing transactions: {e}")

# --- 4. READ FUNCTION (FOR WEB APP - RETURNS DATA) ---
def view_transactions_for_app(conn):
    """Retrieves all transactions and returns them as a list of dictionaries for Streamlit/Pandas."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, amount, category, type FROM transactions ORDER BY date DESC")
        
        # Fetch rows and convert them to dictionaries because of conn.row_factory = sqlite3.Row
        # This fixes the issue by ensuring the data format is consistent for Pandas/Streamlit
        rows = cursor.fetchall() 
        return [dict(row) for row in rows] 
        
    except sqlite3.Error as e:
        # It's helpful to log the error for debugging
        print(f"Error viewing transactions for app: {e}")
        return []

# --- 5. CORE CALCULATION FUNCTION ---
def calculate_total_balance(conn):
    """Calculates the total balance by summing Income and subtracting Expense."""
    try:
        cursor = conn.cursor()
        
        income_query = "SELECT SUM(amount) FROM transactions WHERE type = 'Income'"
        cursor.execute(income_query)
        total_income = cursor.fetchone()[0] or 0.0
        
        expense_query = "SELECT SUM(amount) FROM transactions WHERE type = 'Expense'"
        cursor.execute(expense_query)
        total_expense = cursor.fetchone()[0] or 0.0

        balance = total_income - total_expense
        
        return balance, total_income, total_expense

    except sqlite3.Error as e:
        print(f"Error calculating balance: {e}")
        return 0.0, 0.0, 0.0
        
# --- 6. UPDATE FUNCTION (New) ---
def update_transaction(conn, tx_id, date, amount, category, transaction_type):
    """Updates an existing transaction record."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE transactions
            SET date = ?, amount = ?, category = ?, type = ?
            WHERE id = ?
        """, (date, amount, category, transaction_type, tx_id))
        
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating transaction ID {tx_id}: {e}")
        return False

# --- 7. DELETE FUNCTION (New) ---
def delete_transaction(conn, tx_id):
    """Deletes a transaction record based on its ID."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting transaction ID {tx_id}: {e}")
        return False
    
    # --- 8. RESET FUNCTION (New) ---
def reset_database(conn):
    """Deletes all data from the transactions table."""
    try:
        cursor = conn.cursor()
        # SQL to delete all rows in the table
        cursor.execute("DELETE FROM transactions")
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error resetting database: {e}")
        return False
    


# --- MAIN EXECUTION BLOCK (Cleaned up for app use) ---
if __name__ == "__main__":
    conn = setup_database()
    if conn:
        print(f"Database '{DATABASE_NAME}' set up successfully.")
        
        # Test the core features for terminal output
        view_transactions(conn) 
        
        balance, income, expense = calculate_total_balance(conn)
        print("\n--- FINANCIAL SUMMARY ---")
        print(f"Total Income:  ${income:,.2f}")
        print(f"Total Expense: ${expense:,.2f}")
        print(f"Current Balance: ${balance:,.2f}")
        print("-" * 25)
        
        conn.close()