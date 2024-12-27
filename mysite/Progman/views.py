from django.shortcuts import get_object_or_404, redirect, render
from .models import Progresslvl,Note, PersonalTask

def kanban_board(request):
    # Fetch progress levels with their related tasks
    progress_levels = Progresslvl.objects.prefetch_related('tasks').all()
    return render(request, 'kanban/board.html', {'progress_levels': progress_levels})


def task_notes(request, task_id):
    task = get_object_or_404(PersonalTask, id=task_id)
    note = task.note

    # Create a blank note if it doesn't exist
    if not note:
        note = Note.objects.create(title=f"Notes for {task.project}", user=request.user)
        task.note = note
        task.save()

    return render(request, 'notes/view_note.html', {'note': note})

def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    if request.method == "POST":
        note.content = request.POST.get('content', note.content)
        note.save()
        return redirect('task_notes', task_id=note.task.id)

    return render(request, 'notes/edit_note.html', {'note': note})
