from django.db import models

class Events(models.Model):

    eventUser = models.ForeignKey("EventUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    eventName = models.CharField(max_length=50)
    eventdate = models.DateField(auto_now=False, auto_now_add=False)
    venue = models.CharField(max_length=70)
    numOfGuests = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=100)
    approved = models.BooleanField(default=None)

    # defines the virtual property named by the "related_name" in the foodplanner model and Events serializer
    # Self is referring the object/class we are currently in
    # This code helps to get value
    @property
    def foodplanners(self):
        return self.__foodplanners

# .setter means it changes the value
    @foodplanners.setter
    def foodplanners(self,value):
        self.__foodplanners = value