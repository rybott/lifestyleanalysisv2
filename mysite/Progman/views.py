from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from .models import Matter, Routine, SubRoutine
from .forms import RoutineForm, SubRoutineForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

import calendar
from datetime import datetime

# List all matterstn

class TaskCalendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None, tasks=None):
        super().__init__()
        self.year = year
        self.month = month
        self.tasks = tasks  # Dictionary {day: [task1, task2]}

    def formatday(self, day, weekday):
        """Customize each day cell in the calendar"""
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # Empty day

        task_html = ""
        if day in self.tasks:
            for task in self.tasks[day]:
                task_html += f'<br><span class="task">{task.matter}<br>{task.name}</span> <br> '

        return f'<td class="{self.cssclasses[weekday]}">{day}{task_html}</td>'

    def formatmonth(self, theyear, themonth, withyear=True):
        """Customize the entire month rendering"""
        return f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n' + \
               f"{self.formatmonthname(theyear, themonth, withyear=withyear)}\n" + \
               f"{self.formatweekheader()}\n" + \
               "\n".join(self.formatweek(week) for week in self.monthdays2calendar(theyear, themonth)) + \
               "\n</table>"

class MatterListView(ListView):
    model = Matter
    template_name = 'note/matter_list.html'
    context_object_name = 'matters'

    def get_context_data(self, **kwargs):
        """Inject additional context (calendar) into the template."""
        context = super().get_context_data(**kwargs)

        # Get the current year and month
        now = datetime.now()
        year = self.request.GET.get("year", now.year)
        month = self.request.GET.get("month", now.month)

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            year, month = now.year, now.month

        if month < 1:
                year = year-1
                month = 12
        elif month > 12:
            year = year+1
            month = 1

        # Fetch tasks for this month
        tasks = Routine.objects.filter(due_date__year=year, due_date__month=month)

        # Organize tasks by day
        task_dict = {}
        for task in tasks:
            task_day = task.due_date.day
            if task_day not in task_dict:
                task_dict[task_day] = []
            task_dict[task_day].append(task)

        # Generate the calendar with tasks
        calendar_html = TaskCalendar(year, month, task_dict).formatmonth(year, month)

        # Add to context
        context["calendar"] = calendar_html
        context["year"] = year
        context["month"] = month

        return context


# Show details of a single matter
class MatterDetailView(DetailView):
    model = Matter
    template_name = 'note/matter_detail.html'

# View to load the Routine form
def load_routine_form(request, pk):
    routine = get_object_or_404(Routine, pk=pk)
    if request.method == "POST":
        form = RoutineForm(request.POST, instance=routine)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Routine updated successfully!'})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = RoutineForm(instance=routine)
        html = render_to_string('partials/routine_form.html', {'form': form})
        return JsonResponse({'success': True, 'html': html})

# View to load the SubRoutine form
def load_subroutine_form(request, pk):
    subroutine = get_object_or_404(SubRoutine, pk=pk)
    if request.method == "POST":
        form = SubRoutineForm(request.POST, instance=subroutine)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'SubRoutine updated successfully!'})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SubRoutineForm(instance=subroutine)
        html = render_to_string('partials/subroutine_form.html', {'form': form})
        return JsonResponse({'success': True, 'html': html})
