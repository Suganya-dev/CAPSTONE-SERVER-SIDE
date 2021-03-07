from django.db import models
from django.contrib.auth.models import User

class EventUser(models.Model):

    userId = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=100)
    createdOn = models.DateField(auto_now=False, auto_now_add=False)
    active = models.BooleanField(default=None)
