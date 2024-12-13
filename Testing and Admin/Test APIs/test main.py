import os
import pandas as pd
import duckdb as db
from datetime import datetime
from Transactions import Chase, Discover

'''CHANGES I HAVE MADE
Transactions.py
    - Make the .run def in function

Testmain.py


'''


# Set up Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# import django
# django.setup()

# Prepare the transactions table in DuckDB if it doesn't exist
connection = db.connect('Test_Transdb.duckdb')  # Path to your DuckDB database
connection.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    date DATE,
    account TEXT,
    transaction_type TEXT,
    description TEXT,
    amount FLOAT,
    category_id INTEGER
)
""")


#--------------- Transaction Data -------------------------------------

# Call Functions for Chase and Discover
days = 300  # Assuming you want data for the last 30 days, adjust as needed
Chase_data = Chase.run(day=days)
print("Finished Chase")
Discover_data = Discover.run(day=days)
print("Finished Discover")
transactions_df = pd.concat([Chase_data, Discover_data])
transactions_df['date'] = transactions_df['date'].apply(lambda x: pd.to_datetime(x) if pd.notnull(x) else None)

# Insert recent transactions into DuckDB
# Get the most recent date in transactions_df to use for filtering
min_date = transactions_df['date'].min()

# Query the existing transactions from DuckDB
recent_transactions = connection.execute("""
SELECT date, account, transaction_type, description, amount, category_id
FROM transactions
WHERE date >= ?
""", (min_date,)).fetchall()

# Convert the result into a set for faster lookup
recent_transactions_set = set(recent_transactions)

# Filter out duplicate rows from the dataframe
new_transactions = transactions_df[
    ~transactions_df.apply(
        lambda row: (row['date'], row['account'], row['transaction_type'], row['description'], row['amount'], row['category_id'])
        in recent_transactions_set,
        axis=1
    )
]
print("made ~tranasctions_df")
# Prepare the transactions for bulk insert
insert_query = """
INSERT INTO transactions (date, account, transaction_type, description, amount, category_id)
VALUES (?, ?, ?, ?, ?, ?)
"""

# Execute bulk insert into DuckDB
for _, row in new_transactions.iterrows():
    connection.execute(insert_query, (row['date'], row['account'], row['transaction_type'], row['description'], row['amount'], row['category_id']))

# Optionally, close the connection
connection.close()

print("Finished")

#--------------- News Data -------------------------------------
