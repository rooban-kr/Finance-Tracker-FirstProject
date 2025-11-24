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


def view_transactions(conn):
    """Retrieves and displays all transactions from the database."""
    try:
        cursor = conn.cursor()
        
        # SQL query to select all data, ordered by date
        cursor.execute("SELECT id, date, amount, category, type FROM transactions ORDER BY date DESC")
        
        # Fetch all results returned by the query
        transactions = cursor.fetchall()

        if not transactions:
            print("\nNo transactions found.")
            return

        print("\n--- TRANSACTION HISTORY ---")
        # Print a header for the table
        print(f"{'ID':<4} | {'Date':<10} | {'Type':<8} | {'Category':<15} | {'Amount':>10}")
        print("-" * 50)
        
        # Loop through the results and format them
        for tx in transactions:
            tx_id, date, amount, category, tx_type = tx
            amount_str = f"${amount:,.2f}"
            print(f"{tx_id:<4} | {date:<10} | {tx_type:<8} | {category:<15} | {amount_str:>10}")

    except sqlite3.Error as e:
        print(f"Error viewing transactions: {e}")


def calculate_total_balance(conn):
    """Calculates the total balance by summing Income and subtracting Expense."""
    try:
        cursor = conn.cursor()
        
        # SQL to get the SUM of all Income amounts
        income_query = "SELECT SUM(amount) FROM transactions WHERE type = 'Income'"
        cursor.execute(income_query)
        total_income = cursor.fetchone()[0] or 0.0
        
        # SQL to get the SUM of all Expense amounts
        expense_query = "SELECT SUM(amount) FROM transactions WHERE type = 'Expense'"
        cursor.execute(expense_query)
        total_expense = cursor.fetchone()[0] or 0.0

        # Calculate the net balance
        balance = total_income - total_expense
        
        return balance, total_income, total_expense

    except sqlite3.Error as e:
        print(f"Error calculating balance: {e}")
        return 0.0, 0.0, 0.0


# --- 3. MAIN EXECUTION BLOCK (Last) ---
if __name__ == "__main__":
    conn = setup_database()
    if conn:
        print(f"Database '{DATABASE_NAME}' set up successfully.")
        
        # NOTE: WE ARE COMMENTING OUT THE ADD TRANSACTIONS LINES FOR NOW
        #       This prevents adding duplicates every time you run the script.
        # add_transaction(conn, '2025-11-24', 2500.00, 'Salary', 'Income')
        # add_transaction(conn, '2025-11-24', 55.75, 'Groceries', 'Expense')
        # add_transaction(conn, '2025-11-25', 150.00, 'Rent', 'Expense')
        
        # 1. View all transactions (R - Read)
        view_transactions(conn)
        
        # 2. Calculate and display balance (Core Logic)
        balance, income, expense = calculate_total_balance(conn)
        
        print("\n--- FINANCIAL SUMMARY ---")
        print(f"Total Income:  ${income:,.2f}")
        print(f"Total Expense: ${expense:,.2f}")
        print(f"Current Balance: ${balance:,.2f}")
        print("-" * 25)
        
        conn.close()





