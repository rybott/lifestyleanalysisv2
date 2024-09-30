import os
import django
import pandas as pd

# Must move into the LifestyleAnalysis (inner) folder

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LifestyleAnalysis.settings')  # Replace with your actual settings module
django.setup()

from Finance.models import Categories, Transactions
# Load Categories from the Excel file
categories_df = pd.read_excel('testbed/Historical Transactions/category list.xlsx')

# Load Transactions from the Excel file
transactions_df = pd.read_excel('testbed/Historical Transactions/Historical Transactions.xlsx')

# Ensure all categories in the Excel file are present in the database
for category_name in categories_df['category']:
    # Get or create the category in the database
    category, created = Categories.objects.get_or_create(category=category_name)

# Map categories to their primary keys in the database
category_map = {category.category: category.id for category in Categories.objects.all()}

# Replace category names in transactions with foreign key IDs
transactions_df['category_id'] = transactions_df['category'].map(category_map)

# Drop the original category column
transactions_df.drop(columns=['category'], inplace=True)

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

print("Data imported successfully.")