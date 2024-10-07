from django.db import models

# Create your models here.

class Categories(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category  # Ensure a meaningful string representation of the category
    

class Transactions(models.Model):
    date = models.DateTimeField()
    account = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

'''
# IDs for Categories
[{'id': 1, 'category': 'Amazon'}, 
{'id': 2, 'category': 'Automotive'}, 
{'id': 3, 'category': 'Investment'}, 
{'id': 4, 'category': 'Clothes'}, 
{'id': 5, 'category': 'Dates'}, 
{'id': 6, 'category': 'Education'}, 
{'id': 7, 'category': 'Entertainment'}, 
{'id': 8, 'category': 'Dunkin/Starbucks'}, 
{'id': 9, 'category': 'Gasoline '}, 
{'id': 10, 'category': 'Gifts'}, 
{'id': 11, 'category': 'Government Services'}, 
{'id': 12, 'category': 'Groceries'}, 
{'id': 13, 'category': 'Haircut'}, 
{'id': 14, 'category': 'Lego '}, 
{'id': 15, 'category': 'Medical Services'},
{'id': 16, 'category': 'Merchandise'}, 
{'id': 17, 'category': 'Other Income'}, 
{'id': 18, 'category': 'Pay Check '}, 
{'id': 19, 'category': 'Projects'}, 
{'id': 20, 'category': 'Recurring (mthly)'}, 
{'id': 21, 'category': 'Recurring (yrly)'}, 
{'id': 22, 'category': 'Recurring (Qrtly)'}, 
{'id': 23, 'category': 'Recurring (Other)'}, 
{'id': 24, 'category': 'Restaurants'}, 
{'id': 25, 'category': 'Supermarkets'}, 
{'id': 26, 'category': 'Transportation'}, 
{'id': 27, 'category': 'Other'}, 
{'id': 28, 'category': 'Credit Card Payment'}, 
{'id': 29, 'category': 'Do not Count'}]

Reworking the Database
1. Remove the Categories for Recurring 
2. Put that into the new Recurring Column
    - 0 = Not Recurring [Default]
    - 1 = Monthly
    - 2 = Quartlery
    - Etc.
'''

