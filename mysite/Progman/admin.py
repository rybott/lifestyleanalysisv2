from django.contrib import admin
from .models import Progresslvl, Note, Project, PersonalTask

@admin.register(Progresslvl)
class ProgresslvlAdmin(admin.ModelAdmin):
    list_display = ('level', 'order')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')

@admin.register(PersonalTask)
class PersonalTaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'description', 'level', 'priority', 'is_completed', 'order')
    list_filter = ('level', 'is_completed')
    search_fields = ('project', 'description')
