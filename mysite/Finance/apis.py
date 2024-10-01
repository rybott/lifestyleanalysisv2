from django.shortcuts import render
from django.http import JsonResponse
from .models import Transactions, Categories
from django.db.models import Sum 
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, ExtractYear, ExtractMonth
from django.db.models import F
from datetime import timedelta, date
import calendar

def category_names(request):
    # Get all unique category names from the Categories model
    category_names = Categories.objects.values_list('category', flat=True).distinct()
    
    # Convert to JSON response
    return JsonResponse(list(category_names), safe=False)

def top_5_categories(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    exlude_nocount = request.GET.get('end_date',None)

    transactions = Transactions.objects.all()

    if exlude_nocount:
        transactions = transactions.exclude(category_id = 29)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    # Sum amounts by category and order by total amount
    top_categories = (
        transactions
        .values('category__category')
        .annotate(total_amount=Sum('amount'))
        .order_by('total_amount')[:5]
    )

    # Convert to JSON format
    data = [{'category': item['category__category'], 'total_amount': item['total_amount']} for item in top_categories]
    return JsonResponse(data, safe=False)

def daily_sums(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    exlude_nocount = request.GET.get('exclude_nocount', False)

    transactions = Transactions.objects.all()

    if exlude_nocount:
        transactions = transactions.exclude(category_id = 29)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    daily_totals = transactions.annotate(day=TruncDay('date')).values('date').annotate(total_amount=Sum('amount')).order_by('date')

    data = list(daily_totals)
    return JsonResponse(data, safe=False)

def weekly_sums(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    exlude_nocount = request.GET.get('exclude_nocount', False)

    transactions = Transactions.objects.all()

    if exlude_nocount:
        transactions = transactions.exclude(category_id = 29)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    weekly_totals = transactions.annotate(
        week_start=TruncWeek('date')  # Truncate to the beginning of the week
    ).values('week_start').annotate(
        total_amount=Sum('amount')
    )

    # Convert week_start to the last day of the week (Sunday)
    data = []
    for entry in weekly_totals:
        week_start = entry['week_start']
        week_end = week_start + timedelta(days=6)  # Add 6 days to get to Sunday
        data.append({
            'week_end': week_end,
            'total_amount': entry['total_amount']
        })

    return JsonResponse(data, safe=False)

def monthly_sums(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    exlude_nocount = request.GET.get('exclude_nocount', False)

    transactions = Transactions.objects.all()

    if exlude_nocount:
        transactions = transactions.exclude(category_id = 29)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    monthly_totals = transactions.annotate(
        month_start=TruncMonth('date'),
        year=ExtractYear('date'),
        month=ExtractMonth('date')
    ).values('year', 'month').annotate(
        total_amount=Sum('amount')
    )

    # Convert year and month into the last day of the month
    data = []
    for entry in monthly_totals:
        year = entry['year']
        month = entry['month']
        last_day = calendar.monthrange(year, month)[1]
        last_day_of_month = date(year, month, last_day)
        data.append({
            'month_end': last_day_of_month,
            'total_amount': entry['total_amount']
        })


    return JsonResponse(data, safe=False)