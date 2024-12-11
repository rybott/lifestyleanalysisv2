from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="home"),
    path('login/',views.login, name="login" ),
    path('homepage/', views.homepage, name='homepage'),
]
