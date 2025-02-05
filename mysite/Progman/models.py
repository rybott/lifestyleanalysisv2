from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=250)
    client = models.CharField(max_length=250)
    advisary_corp = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class MatterStatus(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class MatterType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Matter(models.Model):
    name = models.CharField(max_length=250)
    type = models.ForeignKey(MatterType, on_delete=models.SET_NULL, null=True, blank=True, related_name="matters")
    client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="matters")
    start_dte = models.DateField(null=True, blank=True)
    due_dte = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(MatterStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name="matters")
    Percent_complete = models.FloatField(null=True, blank=True)
    final_product = models.FileField(upload_to="documents/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Routine(models.Model):
    name = models.CharField(max_length=250)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, related_name="routine")
    Matter = models.ForeignKey(Matter, on_delete=models.SET_NULL, null=True, blank=True, related_name="routine")
    start_dte = models.DateField(null=True, blank=True)
    due_dte = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, related_name="routine")
    Percent_complete = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class SubRoutine(models.Model):
    name = models.CharField(max_length=250)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, related_name="subroutine")
    Task = models.ForeignKey(Matter, on_delete=models.SET_NULL, null=True, blank=True, related_name="subroutine")
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, related_name="subroutine")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

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
