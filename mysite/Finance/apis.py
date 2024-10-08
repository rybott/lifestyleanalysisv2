from django.shortcuts import render
from django.http import JsonResponse
from .models import Transactions, Categories
from django.db.models import Sum 
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, ExtractYear, ExtractMonth
from django.db.models import F
from datetime import timedelta, date, datetime
import calendar

def category_names(request):
    # Get all unique category names from the Categories model
    category_names = Categories.objects.values_list('category', flat=True).distinct()
    
    # Convert to JSON response
    return JsonResponse(list(category_names), safe=False)

def amount_made(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    
    # Default to last year if no date is specified
    if not start_date:
        current_year = datetime.now().year
        start_date = datetime(current_year, 1, 1).strftime('%Y-%m-%d')

    # Default end date to today if not specified
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')

    transactions = Transactions.objects.filter(date__gte=start_date, date__lte=end_date, category_id=18)

    weekly_totals = transactions.annotate(
        week_start=TruncWeek('date')  # Truncate to the beginning of the week
    ).values('week_start').annotate(
        total_amount=Sum('amount')
    ).order_by('week_start')

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

def daily_expenses(request):
    category_name = request.GET.get('category_name', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    exclude_nocount = request.GET.get('exclude_nocount', False)


    if not start_date:
        one_year_ago = datetime.now() - timedelta(days=365)
        start_date = one_year_ago.strftime('%Y-%m-%d')

    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')

    transactions = Transactions.objects.filter(date__gte=start_date, date__lte=end_date)


    if exclude_nocount:
        transactions = transactions.exclude(category_id=29)
    if category_name:
        category = Categories.objects.get(category=category_name)
        transactions = transactions.filter(category_id=category.id)

    # Filters out positive amounts (i.e. deposits)
    transactions = transactions.filter(amount__lt=0)


    daily_totals = transactions.annotate(day=TruncDay('date')).values('day').annotate(total_amount=Sum('amount')).order_by('day')

    data = list(daily_totals)
    return JsonResponse(data, safe=False)


def weekly_expenses(request):
    category_name = request.GET.get('category_name', None)
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

    if category_name:
        category = Categories.objects.get(category=category_name)
        transactions = transactions.filter(category_id=category.id)

    # Filters out positive amounts (i.e. deposits)
    transactions = transactions.filter(amount__lt=0)

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
            'day': week_end,
            'total_amount': entry['total_amount']
        })

    return JsonResponse(data, safe=False)

def monthly_expenses(request):
    category_name = request.GET.get('category_name', None)
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

    if category_name:
        category = Categories.objects.get(category=category_name)
        transactions = transactions.filter(category_id=category.id)

    # Filters out positive amounts (i.e. deposits)
    transactions = transactions.filter(amount__lt=0)

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
            'day': last_day_of_month,
            'total_amount': entry['total_amount']
        })

    return JsonResponse(data, safe=False)

def top_expenses(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    exlude_nocount = request.GET.get('exclude_nocount', False)

    if not start_date:
        one_year_ago = datetime.now() - timedelta(days=365)
        start_date = one_year_ago.strftime('%Y-%m-%d')

    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')

    category_sums = Transactions.objects.values('category__category').filter(date__gte=start_date, date__lte=end_date).annotate(total_amount=Sum('amount')).order_by('total_amount','category')

    if exlude_nocount:
        category_sums = category_sums.exclude(category_id = 29)

    negative_sum = category_sums.filter(amount__lt=0)
    total_sum = sum(item['total_amount'] for item in negative_sum)

    data = []
    for entry in category_sums:
        category = entry['category__category']
        total_amount = entry['total_amount']
        percent = (total_amount / total_sum) *100
        data.append({
            'Category':category,
            'Amount': f"({abs(round(total_amount, 2)):,.2f})" if total_amount < 0 else f"{round(total_amount, 2):,.2f}",
            'Percent': f"({abs(round(percent, 2)):,.2f})" if percent < 0 else f"{round(percent, 2):,.2f}"
        })
    return JsonResponse(data, safe=False)
