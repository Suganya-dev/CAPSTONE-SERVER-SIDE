from django.db import models

class FoodPlanner(models.Model):

    events = models.ForeignKey("Events", on_delete=models.CASCADE)
    foodTable = models.ForeignKey("FoodTable", related_name="foodtable", on_delete=models.CASCADE)



