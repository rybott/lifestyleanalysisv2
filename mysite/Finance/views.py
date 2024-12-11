from django.shortcuts import render
from django.db.models import Sum
# from django.db.models import F
from datetime import timedelta, date, datetime
import calendar
import json
from django.db.models.functions import Round
import plotly.express as px
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, ExtractYear, ExtractMonth

from .models import Transactions, Categories
from .apis import category_names, top_expenses

def base_testing(request):
    context = {}
    return render(request,'base/base.html',context)

def categorize(request):
    return render(request,'categorize.html',{})

def dashboard3(request):
    context = {}
    # Set default dates if not provided
    today = datetime.now()
    week1_start = today - timedelta(days=7)
    week0_start = week1_start - timedelta(days=7)

    # Setting Filter
    category= request.GET.get('Category_name', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    exlude_nocount = request.GET.get('exlude_nocount', '') == 'on'

    # Weekly Filter
    Chart_type= request.GET.get('chart_type', 'Weekly')

    if not start_date:
        start_date = datetime(today.year, 1, 1).strftime('%Y-%m-%d')
    if not end_date:
        end_date = today.strftime('%Y-%m-%d')


    # Amount Made in Salary over the Period
    Amount_Made = Transactions.objects.filter(date__gte=start_date, date__lte=end_date, category_id=18)
    Amount_Made = Amount_Made.aggregate(total=Sum('amount'))['total'] or 0

    # Amount Spent over the Period and Week Basis
    Amount_Spent_total = Transactions.objects.filter(date__gte=start_date, date__lte=end_date, amount__lt=0)
    Amount_Spent_week1 = Transactions.objects.filter(date__gte=week1_start, date__lte=today, amount__lt=0)
    Amount_Spent_week0 = Transactions.objects.filter(date__gte=week0_start, date__lte=week1_start, amount__lt=0)
    transactions = Amount_Spent_total

    if category:
        worked = "It Worked " + str(category)
        try:
            Category = Categories.objects.get(category=category)
            Amount_Spent_week1 = Amount_Spent_week1.filter(category_id=Category.id)
            Amount_Spent_week0 = Amount_Spent_week0.filter(category_id=Category.id)
            Amount_Spent_total = Amount_Spent_total.filter(category_id=Category.id)
            transactions = transactions.filter(category_id=Category.id)
        except Categories.DoesNotExist:
            worked = f"Category '{category}' does not exist"
    else:
        pass
    if exlude_nocount:
        Amount_Spent_total = Amount_Spent_total.exclude(category_id=29)
        Amount_Spent_week1 = Amount_Spent_week1.exclude(category_id=29)
        Amount_Spent_week0 = Amount_Spent_week0.exclude(category_id=29)
        # transactions = transactions.exclude(category_id=29)

    Amount_Spent_total = Amount_Spent_total.aggregate(total=Sum('amount'))['total'] or 0
    Amount_Spent_week1 = Amount_Spent_week1.aggregate(total=Sum('amount'))['total'] or 0
    Amount_Spent_week0 = Amount_Spent_week0.aggregate(total=Sum('amount'))['total'] or 0

    # Calculate spending change and direction
    Spending_Change = round((Amount_Spent_week1 - Amount_Spent_week0), 2) if Amount_Spent_week0 != 0 else 0.00
    Spending_Direction = "Increase" if (Amount_Spent_week1 - Amount_Spent_week0) >= 0 else "Reduction"

    # Break Down of Exps by Category---------------------------------------
    categories_amount = Transactions.objects.filter(date__gte=start_date, date__lte=end_date) \
        .values('category_id') \
        .annotate(total=Round(Sum('amount'), 2)) \
        .order_by('total')
    # Formatting
    for item in categories_amount:
        item['total'] = round(item['total'], 2)*-1 if item['total'] is not None else 0
        item['total'] = "{:,.2f}".format(item['total'])
    # Map Category Name onto ID
    category_ids = [item['category_id'] for item in categories_amount]
    categories = Categories.objects.filter(id__in=category_ids)
    category_map = {category.id: category.category for category in categories}
    for item in categories_amount:
        item['category_name'] = category_map.get(item['category_id'], 'Unknown')
        spaces = "." * (25 - len(item['category_name']))
        item['category_name'] = item['category_name'] + spaces

    Chart_type= request.GET.get('chart_type', 'Weekly')

    daily_totals = transactions.annotate(day=TruncDay('date')).values('day').annotate(total_amount=Sum('amount')).order_by('day')

    weekly_totals = transactions.annotate(
        week_start=TruncWeek('date')  # Truncate to the beginning of the week
    ).values('week_start').annotate( total_amount=Sum('amount'))

    monthly_totals = transactions.annotate(
        month_start=TruncMonth('date'), year=ExtractYear('date'),month=ExtractMonth('date')).values('year', 'month').annotate(
        total_amount=Sum('amount'))

    if Chart_type == "Daily":
        dates = [entry['day'] for entry in daily_totals]
        totals = [entry['total_amount']*-1 for entry in daily_totals]

    elif Chart_type == "Monthly":
        dates = []
        totals = []
        for entry in monthly_totals:
            year = entry['year']
            month = entry['month']
            last_day = calendar.monthrange(year, month)[1]
            last_day_of_month = date(year, month, last_day)
            dates.append(f"{calendar.month_name[month]} {year}")
            totals.append(entry['total_amount']*-1)

    else:
        # Prepare data for weekly chart
        dates = []
        totals = []
        for entry in weekly_totals:
            week_start = entry['week_start']
            week_end = week_start + timedelta(days=6)  # Get the end of the week (Sunday)
            week_range = f"{week_start.strftime('%b %d, %Y')} - {week_end.strftime('%b %d, %Y')}"
            dates.append(week_range)
            totals.append(entry['total_amount']*-1)

    chart_data = {
        'labels': dates,
        'totals': totals
    }

    context['categories_amount'] = categories_amount
    context['selected_category'] = category
    context['selected_start_date'] = start_date
    context['selected_end_date'] = end_date
    context['Amount_Made'] = round(Amount_Made,2)
    context['Amount_Spent'] = round(Amount_Spent_total*-1,2)
    context['Amount_Spent_week1'] = round(Amount_Spent_week1*-1,2)
    context['Amount_Spent_week0'] = round(Amount_Spent_week0*-1,2)
    context['Spending_change'] = Spending_Change
    context['Spending_direction'] = Spending_Direction
    context['today'] = today
    context['week_start'] = week1_start
    context['exlude_nocount'] = exlude_nocount
    context['chart_data'] = chart_data

    return render(request, 'dashboard v2.html', context)

def exp_breakdown(request):
    pass
