from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from Eventplannerapi.models import FoodType, FoodTable

class FoodtypeSerializer(serializers.ModelSerializer):

    class Meta:
        model= FoodType
        fields = ('id','label')

class FoodtableSerializer(serializers.ModelSerializer):

    foodType = FoodtypeSerializer

    class Meta:
        model = FoodTable
        fields = ('id','label','description','foodType')
        depth =1
    

class FoodtablesView(ViewSet):

    def create(self, request):

        # Handle POST operations
        # Create a new Python instance of the foodtable  class
        # and set its properties from what was sent in the
        # body of the request from the client.
        foodtable = FoodTable()
        foodtable.label = request.data["label"]
        foodtable.description = request.data["description"]
        foodtype = FoodType.objects.get(pk=request.data["foodType"])
        foodtable.foodType=foodtype
        
        # Use the Django ORM to get the record from the database
        # Try to post the newfoodtable  to the database, then
        # serialize thefoodtable  instance as JSON, and send the
        # JSON as a response to the client request

        try:
            foodtable.save()
            serializer = FoodtableSerializer(foodtable, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        # Handle GET requests for singlefoodtable 
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            # The `2` at the end of the route becomes `pk`

            foodtable  = FoodTable.objects.get(pk=pk)
            serializer = FoodtableSerializer(foodtable,many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        # Handle GET requests to foodtable resource

        # Get all foodtable records from the database
        foodtable = FoodTable.objects.all()

        serializer = FoodtableSerializer(
            foodtable, many=True, context={'request': request})
        return Response(serializer.data)


    def update(self, request, pk=None):
        # Handle PUT requests for a foodtable

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of foodtable, get the foodtable record
        # from the database whose primary key is `pk`
        # leftside has to match models/ right side has to match client(postman)
        # below line creates new data in db, ignore that line in update
        # foodtable = FoodTable()
        foodtable = FoodTable.objects.get(pk=pk)

        foodtable.label = request.data["label"]
        foodtable.description = request.data["description"]
        foodtype = FoodType.objects.get(pk=request.data["foodType"])
        foodtable.foodType=foodtype
        foodtable.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)


       
    def destroy(self, request, pk=None):

        try:
            foodtable = FoodTable.objects.get(pk=pk)
            foodtable.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except FoodTable.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

