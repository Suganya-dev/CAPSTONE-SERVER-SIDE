from django.db import models

class FoodType(models.Model):

    label = models.CharField(max_length=500)