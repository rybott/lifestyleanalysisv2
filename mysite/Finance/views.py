from django.shortcuts import render
from django.http import JsonResponse
from .models import Transactions, Categories
from django.db.models import Sum 
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth

def dashboard(request):
    return render(request,'dashboard.html',{})

def categorize(request):
    return render(request,'categorize.html',{})

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
    exlude_nocount = request.GET.get('end_date',None)

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
    exlude_nocount = request.GET.get('end_date',None)

    transactions = Transactions.objects.all()

    if exlude_nocount:
        transactions = transactions.exclude(category_id = 29)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    weekly_totals = transactions.annotate(day=TruncWeek('date')).values('date').annotate(total_amount=Sum('amount')).order_by('date')

    data = list(weekly_totals)
    return JsonResponse(data, safe=False)

def monthly_sums(request):
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

    monthly_totals = transactions.annotate(day=TruncMonth('date')).values('date').annotate(total_amount=Sum('amount')).order_by('date')

    data = list(monthly_totals)
    return JsonResponse(data, safe=False)