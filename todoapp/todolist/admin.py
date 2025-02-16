from django.contrib import admin
from .models import Task, SavedJob


# Register your models here.
admin.site.register(Task)
admin.site.register(SavedJob)