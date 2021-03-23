# File for Model for foodplanner
from django.db import models

class FoodPlanner(models.Model):

    # related_name defines the property to be joined as a virtual property in the foodplanner model.
    # variable name and related_name should not be same
    
    events = models.ForeignKey("Events", on_delete=models.CASCADE)
    foodTable = models.ForeignKey("FoodTable", related_name="foodplanners", on_delete=models.CASCADE)



