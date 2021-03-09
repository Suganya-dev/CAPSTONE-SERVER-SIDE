from django.db import models

class FoodType(models.Model):

    foodType = models.CharField(max_length=250)