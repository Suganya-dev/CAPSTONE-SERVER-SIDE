# View module for handling requests about users
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from Eventplannerapi.models import EventUser

class EventusersView(ViewSet):

    # Handle GET requests for single tag

    def retrieve(self,request,pk=None):

        try:

            eventuser = EventUser.objects.get(pk=pk)
            serializer = EventuserSerializer( eventuser, context = {'request' : request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self,request):

         # Get all eventusers records from the database
        eventuser = EventUser.objects.all()
        serializer = EventuserSerializer(eventuser,many =True,context={'request': request})
        return Response(serializer.data)

class EventuserSerializer(serializers.ModelSerializer):
    # JSON serializer for eventusers

    class Meta:
        model = EventUser
        fields = ('id','user','bio','createdOn','active')
        depth =1
