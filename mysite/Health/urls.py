from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="home"),
    path('addkcal/', views.addkcal, name="addkcal")
]