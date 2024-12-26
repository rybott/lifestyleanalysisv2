from django.urls import path, include
from . import views
from . import apis

urlpatterns = [
    path('base', views.base_testing, name="hometest"),
    path('', views.dashboard3, name="home"),
    path('categorize', views.categorize_transaction, name="categorize_transaction"),
    path('api/category_names/', apis.category_names, name='category-names'),
    path('api/top_5_categories/', apis.top_5_categories, name='top-5-categories'),
    path('api/daily_sums/', apis.daily_expenses, name='daily-sums'),
    path('api/weekly_sums/', apis.weekly_expenses, name='weekly-sums'),
    path('api/monthly_sums/', apis.monthly_expenses, name='monthly-sums'),
    path('api/amount_made/', apis.amount_made, name='amount_made'),
    path('api/top_expenses/', apis.top_expenses, name='top_expenses'),
]
