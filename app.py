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
# NOTE: This calls the specific function we created for the web app
transactions = db.view_transactions_for_app(conn)

if transactions:
    # Convert list of tuples to DataFrame for clean, interactive display
    df = pd.DataFrame(
        transactions, 
        columns=["ID", "Date", "Amount", "Category", "Type"]
    )
    # Highlight income and expense for better visualization
    st.dataframe(
        df.style.applymap(lambda x: 'background-color: #d4edda' if x == 'Income' else 'background-color: #f8d7da', subset=['Type']),
        use_container_width=True
    )
else:
    st.info("No transactions found. Use the form above to add one!")

# The connection is automatically closed when the Streamlit script finishes execution
# You can remove the conn.close() line we previously used in tracker.py's main block.