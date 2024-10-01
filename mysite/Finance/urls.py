from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="home"),
    path('categorize', views.categorize, name="categorize"),
    path('api/category_names/', views.category_names, name='category-names'),
    path('api/top_5_categories/', views.top_5_categories, name='top-5-categories'),
    path('api/daily_sums/', views.daily_sums, name='daily-sums'),
    path('api/weekly_sums/', views.weekly_sums, name='weekly-sums'),
    path('api/monthly_sums/', views.monthly_sums, name='monthly-sums'),
]