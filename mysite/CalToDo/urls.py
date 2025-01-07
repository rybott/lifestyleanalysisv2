from django.urls import path
from . import views

urlpatterns = [
    path('get-calendar-data/', views.get_calendar_data, name='get_calendar_data'),
    path('',views.rendercal,name='rendercal'),
    path('add-event/', views.add_event, name='add_event'),
    path('update-event/', views.update_event, name='update_event'),
    path('save-event/', views.save_event, name='save_event'),
    path('delete-event/', views.delete_event, name='delete_event'),
]
