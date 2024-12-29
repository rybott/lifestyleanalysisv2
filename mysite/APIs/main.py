import os
import sys
import django
from django.utils.timezone import make_aware

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Your imports
import pandas as pd
from Finance.models import Transactions
from transactions_import import Chase, Discover
print(f'Chase: {Chase}, Discover: {Discover}')
from django.db import transaction


#--------------- Transaction Data -------------------------------------

# Call Functions for Chase and Discover
days = 1
failures = 0

try:
    Chase_data = Chase().Get(day=days)
except Exception as e:
    print(f'Error in Chase: {e}')
    Chase_data = pd.DataFrame()
    failures += 1

try:
    Discover_data = Discover().Get(day=days)
except Exception as e:
    print(f'Error in Discover: {e}')
    Discover_data = pd.DataFrame()
    failures += 1

if failures == 2:
    print("System dead")
    sys.exit(1)

transactions_df = pd.concat([Chase_data,Discover_data])

current_dir = os.path.dirname(os.path.abspath(__file__))
excel_file_path = os.path.join(current_dir, "AutoCategory.xlsx")
category_map = pd.read_excel(excel_file_path, header=None, names=['text', 'id'])

mapping_dict = category_map.set_index('text')['id'].to_dict()

def map_category(description):
    if pd.isna(description):
        return 30
    description_lower = description.lower()
    for text, category_id in mapping_dict.items():
        if text.lower() in description_lower:
            return category_id
    return 30


transactions_df ['category_id'] = transactions_df ['description'].apply(map_category)
transactions_df['date'] = transactions_df['date'].apply(lambda x: make_aware(x) if pd.notna(x) else x)

transactions_df['amount'] = transactions_df.apply(
    lambda row: row['amount'] * -1 if 'deposit' not in row['description'].lower() else row['amount'],
    axis=1
)

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
with transaction.atomic():
    Transactions.objects.bulk_create(transaction_objects)


#--------------- News Data -------------------------------------
