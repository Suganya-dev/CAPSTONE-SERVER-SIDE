# File for Model for foodplanner
from django.db import models

class FoodPlanner(models.Model):

    # related_name defines the property to be joined as a virtual property in the foodplanner model.

    events = models.ForeignKey("Events", on_delete=models.CASCADE)
    foodTable = models.ForeignKey("FoodTable", related_name="foodTable", on_delete=models.CASCADE)



