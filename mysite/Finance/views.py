from django.shortcuts import render
from django.http import JsonResponse
from .models import Transactions, Categories
from django.db.models import Sum 
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, ExtractYear, ExtractMonth
from django.db.models import F
from datetime import timedelta, date, datetime
import calendar
import json
from decimal import Decimal

from .apis import category_names, top_expenses

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()  # Convert datetime to string in ISO format
        return super().default(obj)

def base_testing(request):
    context = {}
    if request.method == 'GET':
        context['selected_category'] = request.GET.get('Category_name', '')
        context['selected_start_date'] = request.GET.get('start_date', '')
        context['selected_end_date'] = request.GET.get('end_date', '')
        context['exlude_nocount'] = 'checked' if request.GET.get('exlude_nocount') == 'on' else ''
    

    return render(request,'base/base.html',context)

import json
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, ExtractYear, ExtractMonth
from django.shortcuts import render
from datetime import datetime, timedelta, date
import calendar

import json
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, ExtractYear, ExtractMonth
from django.shortcuts import render
from datetime import datetime, timedelta, date
import calendar

def dashboard2(request):
    context = {}
    
    # Extract filters from the GET request
    category = request.GET.get('Category_name', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    exlude_nocount = request.GET.get('exlude_nocount', '') == 'on'

    # Set default dates if not provided
    today = datetime.now()
    week1_start = today - timedelta(days=7)
    week0_start = week1_start - timedelta(days=7)
    
    if not start_date:
        start_date = datetime(today.year, 1, 1).strftime('%Y-%m-%d')
    if not end_date:
        end_date = today.strftime('%Y-%m-%d')

    # QuerySet for income and expenses
    Amount_Made = Transactions.objects.filter(date__gte=start_date, date__lte=end_date, category_id=18)
    Amount_Spent_total = Transactions.objects.filter(date__gte=start_date, date__lte=end_date, amount__lt=0)
    Amount_Spent_week1 = Transactions.objects.filter(date__gte=week1_start, date__lte=today, amount__lt=0)
    Amount_Spent_week0 = Transactions.objects.filter(date__gte=week0_start, date__lte=week1_start, amount__lt=0)
    
    # If a category is selected, filter by category
    if category:
        worked = "It Should have Worked " + str(category)
        try:
            Category = Categories.objects.get(category=category)
            Amount_Spent_week1 = Amount_Spent_week1.filter(category_id=Category.id)
            Amount_Spent_week0 = Amount_Spent_week0.filter(category_id=Category.id)
            Amount_Spent_total = Amount_Spent_total.filter(category_id=Category.id)
        except Categories.DoesNotExist:
            worked = f"Category '{category}' does not exist"
    else:
        worked = "It didn't work"

    # Exclude 'nocount' category if checkbox is checked
    if exlude_nocount:
        Amount_Spent_total = Amount_Spent_total.exclude(category_id=29)
        Amount_Spent_week1 = Amount_Spent_week1.exclude(category_id=29)
        Amount_Spent_week0 = Amount_Spent_week0.exclude(category_id=29)

    # Aggregate totals
    Amount_Spent_total = Amount_Spent_total.aggregate(total=Sum('amount'))['total'] or 0
    Amount_Spent_week1 = Amount_Spent_week1.aggregate(total=Sum('amount'))['total'] or 0
    Amount_Spent_week0 = Amount_Spent_week0.aggregate(total=Sum('amount'))['total'] or 0
    Amount_Made = Amount_Made.aggregate(total=Sum('amount'))['total'] or 0

    # Calculate spending change and direction
    Spending_Change = round((Amount_Spent_week1 - Amount_Spent_week0), 2) if Amount_Spent_week0 != 0 else 0.00
    Spending_Direction = "Increase" if (Amount_Spent_week1 - Amount_Spent_week0) >= 0 else "Reduction"

    # Creating Context
    context['worked'] = worked
    context['today'] = today
    context['week_start'] = week1_start
    context['Amount_Made'] = round(Amount_Made,2)
    context['Amount_Spent'] = round(Amount_Spent_total*-1,2)
    context['Amount_Spent_week1'] = round(Amount_Spent_week1*-1,2)
    context['Amount_Spent_week0'] = round(Amount_Spent_week0*-1,2)
    context['Spending_change'] = Spending_Change
    context['Spending_direction'] = Spending_Direction
    context['selected_category'] = category
    context['selected_start_date'] = start_date
    context['selected_end_date'] = end_date
    context['exlude_nocount'] = exlude_nocount

    return render(request, 'dashboard v2.html', context)

def categorize(request):
    return render(request,'categorize.html',{})

