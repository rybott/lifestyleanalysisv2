from django.urls import path
from .views import get_calendar_data, rendercal

urlpatterns = [
    path('get-calendar-data/', get_calendar_data, name='get_calendar_data'),
    path('',rendercal,name='rendercal')
]
