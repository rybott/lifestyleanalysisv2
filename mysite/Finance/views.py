from django.shortcuts import render
from django.http import JsonResponse
from .models import Transactions, Categories
from django.db.models import Sum 
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, ExtractYear, ExtractMonth
from django.db.models import F
from datetime import timedelta, date, datetime
import calendar
from .apis import category_names

def base_testing(request):
    context = {}
    if request.method == 'GET':
        context['selected_category'] = request.GET.get('Category_name', 'All Categories')
        context['selected_start_date'] = request.GET.get('start_date', '')
        context['selected_end_date'] = request.GET.get('end_date', '')
        context['exlude_nocount'] = 'checked' if request.GET.get('exlude_nocount') == 'on' else ''
    

    return render(request,'base/base.html',context)

def dashboard2(request):
    context = {}
    if request.method == 'GET':

        category = request.GET.get('Category_name', 'All Categories')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        exlude_nocount = 'checked' if request.GET.get('exlude_nocount') == 'on' else ''

        today = datetime.now()
        week1_start = today - timedelta(days=7)
        week0_start = week1_start - timedelta(days=7)
    
        if not start_date:
            current_year = datetime.now().year
            start_date = datetime(current_year, 1, 1).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
    
        Amount_Made = Transactions.objects.filter(date__gte=start_date, date__lte=end_date, category_id=18).aggregate(total=Sum('amount'))['total'] or 0 
        Amount_Spent = Transactions.objects.filter(date__gte=start_date, date__lte=end_date, amount__lt=0).aggregate(total=Sum('amount'))['total'] or 0 
        Amount_Spent_week1 = Transactions.objects.filter(date__gte=week1_start, date__lte=today, amount__lt=0).aggregate(total=Sum('amount'))['total'] or 0  
        Amount_Spent_week0 = Transactions.objects.filter(date__gte=week0_start, date__lte=week1_start, amount__lt=0).aggregate(total=Sum('amount'))['total'] or 0  
        
        if category != "All Categories":
            category = Categories.objects.get(category=category)
            Amount_Spent_week1 = Transactions.objects.filter(date__gte=week1_start, date__lte=today, amount__lt=0, category_id=category.id).aggregate(total=Sum('amount'))['total'] or 0  
            Amount_Spent_week0 = Transactions.objects.filter(date__gte=week0_start, date__lte=week1_start, amount__lt=0, category_id=category.id).aggregate(total=Sum('amount'))['total'] or 0  

                

        Spending_Change = f"({abs(round((Amount_Spent_week1 - Amount_Spent_week0), 2)):,.2f})" if  Amount_Spent_week0 != 0 else "0.00"
        Spending_Direction = "Increase" if (Amount_Spent_week1 - Amount_Spent_week0) >= 0 else "Reduction"

        Amount_Made = f"{round(Amount_Made, 2):,.2f}"
        Amount_Spent_week0 = f"({abs(round(Amount_Spent_week0, 2)):,.2f})" if Amount_Spent_week0 < 0 else f"{round(Amount_Spent_week0, 2):,.2f}"
        Amount_Spent_week1 = f"({abs(round(Amount_Spent_week1, 2)):,.2f})" if Amount_Spent_week1 < 0 else f"{round(Amount_Spent_week1, 2):,.2f}"
        Amount_Spent = f"({abs(round(Amount_Spent, 2)):,.2f})" if Amount_Spent < 0 else f"{round(Amount_Spent, 2):,.2f}"



        context['today'] = today
        context['week_start'] = week1_start
        context['Amount_Made'] = Amount_Made
        context['Amount_Spent'] = Amount_Spent 
        context['Amount_Spent_week1'] = Amount_Spent_week1
        context['Amount_Spent_week0'] = Amount_Spent_week0
        context['Spending_change'] = Spending_Change
        context['Spending_direction'] = Spending_Direction
        context['selected_category'] = category
        context['selected_start_date'] = start_date
        context['selected_end_date'] = end_date
        context['exlude_nocount'] = exlude_nocount
        

    return render(request,'dashboard v2.html',context)

def categorize(request):
    return render(request,'categorize.html',{})

