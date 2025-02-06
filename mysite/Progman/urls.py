from django.urls import path
from . import views

urlpatterns = [
    path('matters/', views.MatterListView.as_view(), name='matter_list'),
    path('matters/<int:pk>/', views.MatterDetailView.as_view(), name='matter_detail'),
    path('routine/<int:pk>/edit/', views.load_routine_form, name='edit_routine'),
    path('subroutine/<int:pk>/edit/', views.load_subroutine_form, name='edit_subroutine'),
]
