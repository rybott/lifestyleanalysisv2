from django.contrib import admin
from .models import Matter, Routine, SubRoutine, Note, Client, MatterStatus, MatterType, Status, Type

admin.site.register(Matter)
admin.site.register(Routine)
admin.site.register(SubRoutine)
admin.site.register(Note)
admin.site.register(Client)
admin.site.register(MatterStatus)
admin.site.register(MatterType)
admin.site.register(Status)
admin.site.register(Type)
