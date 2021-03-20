# View module for handling requests about events
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from Eventplannerapi.models import EventUser,Category,Events,FoodTable,FoodPlanner
from django.contrib.auth.models import User
from rest_framework.decorators import action

class EventsView(ViewSet):

    def create(self,request):
        # Handle POST operations
        # the one which user is logged in
        event_user = EventUser.objects.get(user=request.auth.user)

        events = Events()
        events.eventName = request.data["eventName"]
        events.eventdate = request.data["eventdate"]
        events.venue = request.data["venue"]
        events.numOfGuests= request.data["numOfGuests"]
        events.content = request.data["content"]
        events.approved = True
        category = Category.objects.get(pk= request.data["category"])
        events.category = category
        events.eventUser = event_user

        try:
            events.save()
            serializer = EventsSerializer(events, context={'request':request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods = ['post','delete'], detail =True)
    # detail = True targetting single data
    # detail =false It targets whole object
    def foodplanner(self,request,pk=None):

        if request.method == "POST":

            events = Events.objects.get(pk=pk)
            food_Table = FoodTable.objects.get(id =request.data["foodTable_id"])
            try:
              planning = FoodPlanner.objects.get( events=events, foodTable=food_Table)
              return Response(
                  {'message' : 'This foodplanner is on the Events'},
                  status = status.HTTP_422_UNPROCESSABLE_ENTITY)

            except FoodPlanner.DoesNotExist:
                foodplanner = FoodPlanner()
                foodplanner.events = events
                foodplanner.foodTable = food_Table
                foodplanner.save()
                return Response ({}, status=status.HTTP_201_CREATED)

        elif request.method =="DELETE":
            try:
               
                
                events = Events.objects.get(pk=pk)
                food_Table = self.request.query_params.get('foodTableId', None)

            except Events.DoesNotExist:
                return Response(
                    {'message' : "event does not exist."},
                    status = status.HTTP_400_BAD_REQUEST)

            try:
                planning = FoodPlanner.objects.get( events=events, foodTable=food_Table)
                planning.delete()

                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except FoodPlanner.DoesNotExist:
                return Response(
                    {'message': 'Foodplanner is not on the Events'},
                    status = status.HTTP_404_NOT_FOUND
                    )

        # If the client performs a request other than given methods,It will return this message
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # method to get all the data from API
        # Handles GET operation

    def list(self,request):

        events = Events.objects.all()

        serializer = EventsSerializer (events, many=True, context={'request': request})

        return Response(serializer.data)

        # method to get Single data from API

    def retrieve(self, request, pk=None):

        event_user = EventUser.objects.get(user=request.auth.user)

        try:

            events= Events.objects.get(pk=pk)

            foodtable = FoodTable.objects.filter(foodplanner__events = events)

            jointserializer = FoodtableSerializer(foodtable, many=True, context = {'request':request})
         


            # serializer.data is immutatble,so i made a copy 
            # many=true, many objects, array of objects
            # many =false, if you are having one object

            serializer = EventsSerializer (events, many=False, context={'request': request})
            data = serializer.data
            data["foodtable"] = jointserializer.data
            return Response(data)
        except Exception as ex:
            return HttpResponseServerError(ex)

            

    def update(self, request, pk=None):
        # Handle PUT requests for a events

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of events, get the events record
        # from the database whose primary key is `pk`
        # leftside has to match models/ right side has to match client(postman)
        
        # below line creates a new instance, create a new data in DB, we dont want that in
        # update fn
        # events = Events()

        event_user = EventUser.objects.get(user=request.auth.user)
        events = Events.objects.get(pk=pk)
        
        events.eventName = request.data["eventName"]
        events.eventdate = request.data["eventdate"]
        events.venue = request.data["venue"]
        events.numOfGuests = request.data["numOfGuests"]
        events.content = request.data["content"]
        events.approved= True
        category = Category.objects.get(pk= request.data["category"])
        events.category = category
        events.eventUser = event_user
        events.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single event

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            events = Events.objects.get(pk=pk)
            events.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Events.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EventuserSerializer(serializers.ModelSerializer):

    class Meta:

        model = EventUser
        fields = ['id','bio','user']
        depth = 1

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id","label"]


class EventsSerializer(serializers.ModelSerializer):

    # many=false is for getting single value
    # many = true is for getting all values

    category = CategorySerializer(many=False)
    eventUser = EventuserSerializer(many=False)

    class Meta:
        model = Events
        fields = ('id','eventName','eventdate','venue','numOfGuests','content','approved','category','eventUser')
        # depth = 1


class FoodtableSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodTable
        fields = ('id','label','description')
# if the data not in the DB, but we need it in Models,then its called Custom property in models
#  and custom actions in Views

class FoodplannerSerializer(serializers.ModelSerializer):

    events = EventsSerializer(many=True)
    foodTable = FoodtableSerializer(many=True)

    class Meta:
        model = FoodPlanner
        fields = ('id','events','foodTable')
        depth = 2