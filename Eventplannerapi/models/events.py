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

    @property
    def foodTable(self):
        return self.__foodTable

    @foodTable.setter
    def foodTable(self,value):
        self.__foodTable = value