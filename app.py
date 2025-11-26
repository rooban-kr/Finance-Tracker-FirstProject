import streamlit as st
import tracker as db  # Import your logic file
import pandas as pd

# Define the database name (must match tracker.py)
DATABASE_NAME = 'finance_data.db'
conn = db.setup_database()

# Set page layout to wide for better visualization
st.set_page_config(layout="wide")

## --- Title and Summary ---
st.title("💰 Simple Personal Finance Tracker")

# 1. Calculate Summary (Uses the function you just implemented!)
balance, income, expense = db.calculate_total_balance(conn)

st.subheader("Current Financial Overview")
col1, col2, col3 = st.columns(3)

# Display key metrics
col1.metric("Total Income", f"${income:,.2f}", delta_color="inverse")
col2.metric("Total Expense", f"${expense:,.2f}", delta_color="inverse")
col3.metric("Current Balance", f"${balance:,.2f}")

# Add a reset button section
st.markdown("---")
st.subheader("Database Management")
if st.button("🔴 Reset All Data (Delete All Transactions)", help="CAUTION: This will permanently delete all records!"):
        if db.reset_database(conn):
            st.success("Database successfully reset! All transactions deleted.")
            st.rerun()
        else:
            st.error("Failed to reset database.")

st.markdown("---")

## --- Add Transaction Form ---
st.header("➕ Add New Transaction")
with st.form("new_transaction"):
    
    # Input Fields
    date = st.date_input("Date")
    transaction_type = st.selectbox("Type", ["Income", "Expense"])
    category = st.text_input("Category (e.g., Salary, Rent, Groceries)", value="")
    amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f")

    submitted = st.form_submit_button("Add Transaction")
    
    # Handle Submission
    if submitted:
        if category.strip() and amount > 0:
            db.add_transaction(
                conn, 
                str(date), # Convert date to string for SQLite
                float(amount), 
                category.strip(), # Remove extra spaces
                transaction_type
            )
            st.success(f"{transaction_type} of ${amount:,.2f} recorded successfully!")
            # Rerun the app to update the display
            st.rerun() 
        else:
            st.error("Please ensure Category and Amount are entered correctly.")
            
st.markdown("---")

## --- Display History ---
st.header("🗒️ Transaction History")

# Get transactions from the database

transactions = db.view_transactions_for_app(conn)

if transactions:
    # Convert list of dictionaries (from tracker.py) to DataFrame 
    df = pd.DataFrame(transactions)
    
    # CRITICAL FIX: Ensure the column order and names are correctly mapped
    df = df[['id', 'date', 'amount', 'category', 'type']] 
    df.columns = ["ID", "Date", "Amount", "Category", "Type"] # Set display names

    # Display transaction history with clean formatting
    st.dataframe(
        df.style.format({
            # Enforce 2 decimal places and use commas for thousands
            "Amount": "₹{:,.2f}".format 
        }),
        use_container_width=True
    )
    
# ... rest of the app.py file
else:
    st.info("No transactions found. Use the form above to add one!")

# The connection is automatically closed when the Streamlit script finishes execution
# You can remove the conn.close() line we previously used in tracker.py's main block.