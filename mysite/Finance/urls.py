from django.urls import path
from . import views
from . import apis

urlpatterns = [
    path('', views.dashboard, name="home"),
    path('categorize', views.categorize, name="categorize"),
    path('api/category_names/', apis.category_names, name='category-names'),
    path('api/top_5_categories/', apis.top_5_categories, name='top-5-categories'),
    path('api/daily_sums/', apis.daily_sums, name='daily-sums'),
    path('api/weekly_sums/', apis.weekly_sums, name='weekly-sums'),
    path('api/monthly_sums/', apis.monthly_sums, name='monthly-sums'),
]