from django.shortcuts import render
from django.http import JsonResponse
from .models import Transactions, Categories
from django.db.models import Sum 
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, ExtractYear, ExtractMonth
from django.db.models import F
from datetime import timedelta, date
import calendar
from .apis import category_names

def dashboard(request):
    context = {}
    if request.method == 'GET':
        context['selected_category'] = request.GET.get('Category_name', 'All Categories')
        context['selected_start_date'] = request.GET.get('start_date', '')
        context['selected_end_date'] = request.GET.get('end_date', '')
        context['exlude_nocount'] = 'checked' if request.GET.get('exlude_nocount') == 'on' else ''
    

    return render(request,'dashboard.html',context)

def categorize(request):
    return render(request,'categorize.html',{})

