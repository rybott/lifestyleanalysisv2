from django import forms
from .models import Routine, SubRoutine

class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = [
            'name', 'type', 'start_date', 'due_date',
            'description', 'status', 'percent_complete'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SubRoutineForm(forms.ModelForm):
    class Meta:
        model = SubRoutine
        fields = ['name', 'type', 'description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
