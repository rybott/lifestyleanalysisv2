from django.urls import path
from . import views

urlpatterns = [
    path('kanban/', views.kanban_board, name='kanban_board'),
    path('note/<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('task/<int:task_id>/notes/', views.task_notes, name='task_notes'),
]
