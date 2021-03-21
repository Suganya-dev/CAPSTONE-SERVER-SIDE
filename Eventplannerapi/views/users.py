"""View module for handling requests about tags"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.db.models.functions import Lower
from rest_framework.viewsets import ViewSet
from Eventplannerapi.models import EventUser

class UsersView(ViewSet):

    def retrieve(self,request,pk=None):

        "Handles GET request for single tag"
        # get single users from database
        try:
            user = EventUser.objects.get(pk=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self,request):

        "Handles GET request for all tags"

        # Get all users from the database
        user = EventUser.objects.all()
        serializers = UserSerializer(user, many=True, context = {'request': request})
        return Response(serializers.data)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventUser
        fields = ('id','user','bio','createdOn','active')
        depth =1









