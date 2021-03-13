# View module for handling requests about events
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from Eventplannerapi.models import EventUser,Category,Events
from django.contrib.auth.models import User

class EventsView(ViewSet):

    def create(self,request):
        # Handle POST operations

        event_user = EventUser.objects.get(user=request.auth.user)

        events = Events()
        events.eventName = request.data["eventName"]
        events.eventdate = request.data["eventdate"]
        events.venue = request.data["venue"]
        events.numOfGuests= request.data["numOfGuests"]
        events.content = request.data["content"]
        events.approved = True
        category = Category.objects.get(pk=request.data["category"])
        events.category = category
        events.user = event_user

        try:
            events.save()
            serializer = EventsSerializer(events, context={'request':request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def list(self,request):

        events = Events.objects.all()

        serializer = EventsSerializer (events, many=True, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        # event_user = EventUser.objects.get(user=request.auth.user)

        try:

            events= Events.objects.get(pk=pk)

            
            # if events.user_id ==   event_user.id:
            #     events.is_current_user = True
            # else:
            #     events.is_current_user = False

            serializer = EventsSerializer (events, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class EventuserSerializer(serializers.ModelSerializer):

    class Meta:

        model = EventUser
        fields = ['id','bio','user']
        depth = 1

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("label")

class EventsSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True)
    eventusers = EventuserSerializer(many=False)

class Meta:
    model = Events
    fields = ("id",'eventName','eventdate','venue','numOfGuests','content',
    'approved','categories','eventusers')
    # depth = 2

