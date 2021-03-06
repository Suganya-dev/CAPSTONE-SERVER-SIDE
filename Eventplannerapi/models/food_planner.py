from django.db import models

class FoodPlanner(models.Model):

    eventsId = models.ForeignKey("Events", related_name="events", on_delete=models.CASCADE)
    food_label= models.CharField(max_length=100)
    food_TableId=models.ForeignKey("FoodTable", related_name="foodtable", on_delete=models.CASCADE)


