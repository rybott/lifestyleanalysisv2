from django.db import models
from django.contrib.auth.models import User
import markdown


class Progresslvl(models.Model):
    level = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)  # Controls the sequence of progress levels

    class Meta:
        ordering = ['order']  # Default ordering by the `order` field

    def __str__(self):
        return self.level


class Note(models.Model):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)  # Markdown content
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def render_html(self):
        return markdown.markdown(self.content)

    def __str__(self):
        return self.title or f"Note {self.id}"


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #
    note = models.OneToOneField(Note, null=True, blank=True, on_delete=models.SET_NULL, related_name="project")

    def __str__(self):
        return self.name


class PersonalTask(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    project = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    level = models.ForeignKey(Progresslvl, on_delete=models.CASCADE, related_name="tasks")
    note = models.OneToOneField(Note, null=True, blank=True, on_delete=models.SET_NULL, related_name="task")  # Linked note
    url = models.URLField(null=True, blank=True)
    priority = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.project}: {self.description[:50]}..."
