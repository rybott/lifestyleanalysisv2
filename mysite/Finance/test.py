from django.shortcuts import render
from django.http import JsonResponse
from .models import Transactions, Categories
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, ExtractYear, ExtractMonth
from django.db.models import F
from datetime import timedelta, date, datetime
import calendar
import plotly.express as px

def daily_expenses(request):
    category_name = request.GET.get('category_name', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    exclude_nocount = request.GET.get('exclude_nocount', False)
    transactions = transactions.filter(amount__lt=0)

    # Only What is below this point is needed

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
        totals = [entry['total_amount'] for entry in daily_totals]
        fig = px.line(
            x=dates,
            y=totals,
            labels={'x': 'Date', 'y': 'Amount ($)'},
            title='Daily Expenses'
        )
    elif Chart_type == "Monthly":
        months = []
        totals = []
        for entry in monthly_totals:
            year = entry['year']
            month = entry['month']
            last_day = calendar.monthrange(year, month)[1]
            last_day_of_month = date(year, month, last_day)
            months.append(f"{calendar.month_name[month]} {year}")
            totals.append(entry['total_amount'])
        fig = px.line(
            x=months,
            y=totals,
            labels={'x': 'Month', 'y': 'Amount ($)'},
            title='Monthly Expenses'
        )
    else:
        # Prepare data for weekly chart
        weeks = []
        totals = []
        for entry in weekly_totals:
            week_start = entry['week_start']
            week_end = week_start + timedelta(days=6)  # Get the end of the week (Sunday)
            week_range = f"{week_start.strftime('%b %d, %Y')} - {week_end.strftime('%b %d, %Y')}"
            weeks.append(week_range)
            totals.append(entry['total_amount'])
        fig = px.line(
            x=weeks,
            y=totals,
            labels={'x': 'Week', 'y': 'Amount ($)'},
            title='Weekly Expenses'
        )
    chart = fig.to_html()






    return JsonResponse("", safe=False)
