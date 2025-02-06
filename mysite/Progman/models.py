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
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="matters")
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True) # Put your Notes Here
    status = models.ForeignKey(MatterStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name="matters")
    percent_complete = models.FloatField(null=True, blank=True)
    final_product = models.FileField(upload_to="documents/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Routine(models.Model):
    name = models.CharField(max_length=250)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, related_name="routines")
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE, related_name="routines")
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True) # Put your Notes Here
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, related_name="routines")
    percent_complete = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SubRoutine(models.Model):
    name = models.CharField(max_length=250)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, related_name="subroutines")
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name="subroutines")
    description = models.TextField(null=True, blank=True) # Put your Notes Here
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Note(models.Model):
    content = models.TextField()  # The actual note
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE, related_name="notes", null=True, blank=True)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name="notes", null=True, blank=True)
    subroutine = models.ForeignKey(SubRoutine, on_delete=models.CASCADE, related_name="notes", null=True, blank=True)

    def __str__(self):
        return f"Note ({self.created_at})"
