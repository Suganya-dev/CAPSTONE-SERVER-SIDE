from django.db import models

class FoodTable(models.Model):

    label = models.CharField(max_length=50)
    description = models.CharField(max_length =100)
