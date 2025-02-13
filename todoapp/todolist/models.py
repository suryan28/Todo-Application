from django.db import models
from django.contrib.auth.models import User



class Task(models.Model):
    title=models.CharField(max_length=350)
    completed=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)

    
    def __str__(self):
        self.title