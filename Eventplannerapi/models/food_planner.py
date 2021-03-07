from django.db import models

class FoodPlanner(models.Model):

    eventsId = models.ForeignKey("Events", related_name="events", on_delete=models.CASCADE)
    foodLabel = models.CharField(max_length=100)
    foodTableId = models.ForeignKey("FoodTable", related_name="foodtable", on_delete=models.CASCADE)


