import os
import django
import pandas as pd
from django.utils import timezone
from Finance.models import Transactions
from Transactions import Chase, Discover


# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()


#--------------- Transaction Data -------------------------------------

# Call Functions for Chase and Discover
days =  

Chase_data = Chase(days)
Discover_data = Discover(days)
transactions_df = pd.concat(['Chase_data','Discover_data'])
transactions_df['date'] = transactions_df['date'].apply(lambda x: timezone.make_aware(x) if pd.notnull(x) else None)

min_date = transactions_df['date'].min()
recent_transactions = Transactions.objects.filter(date__gte=min_date).values_list(
    'date', 'account', 'transaction_type', 'description', 'amount', 'category_id'
)

# Convert to a set for faster lookup
recent_transactions_set = set(recent_transactions)

# Filter out duplicate rows
recent_transactions_set = set(recent_transactions)
new_transactions = transactions_df[
    ~transactions_df.apply(
        lambda row: (row['date'], row['account'], row['transaction_type'], row['description'], row['amount'], row['category_id'])
        in recent_transactions_set,
        axis=1
    )
]

# Prepare transactions for bulk insert
transaction_objects = [
    Transactions(
        date=row['date'],
        account=row['account'],
        transaction_type=row['transaction_type'],
        description=row['description'],
        amount=row['amount'],
        category_id=row['category_id'],
    )
    for _, row in transactions_df.iterrows()
]

# Bulk insert transactions into the database
Transactions.objects.bulk_create(transaction_objects)

#--------------- News Data -------------------------------------
