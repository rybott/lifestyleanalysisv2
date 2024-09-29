from django.db import models

# Create your models here.

class Categories(models.Model):
    category = models.CharField(max_length=50)

class Transactions(models.Model):
    date = models.DateTimeField()
    account = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
