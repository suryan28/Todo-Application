from django.db import models
from django.contrib.auth.models import User



class Task(models.Model):
    title=models.CharField(max_length=350)
    completed=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)

    
    def __str__(self):
        self.title

class SavedJob(models.Model):
    title = models.CharField(max_length=350)
    company = models.CharField(max_length=255)  # Fixed capitalization
    location = models.CharField(max_length=255)
    date_posted = models.CharField(max_length=100)
    job_url = models.URLField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title