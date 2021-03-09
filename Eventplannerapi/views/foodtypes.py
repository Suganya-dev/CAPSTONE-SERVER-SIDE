"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from Eventplannerapi.models import FoodType

class FoodtypesView(ViewSet):

    def create(self, request):
        foodtype = FoodType()

        foodtype.label = request.data['foodType']

        try:
            foodtype.save()
            serializer = FoodTypeSerializer(
                foodtype, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

            # this will handle request for a single foodtype

    def retrieve(self, request, pk=None):

        try:
            foodtype = FoodType.objects.get(pk=pk)
            serializer = FoodTypeSerializer(
                foodtype, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        foodtype = FoodType.objects.all()

        ordered_posts = foodtype.order_by('foodType')

        serializer = FoodTypeSerializer(
            ordered_posts, many=True, context={'request': request})
        return Response(serializer.data)

    # This will handle the edit of a foodtype

    def update(self, request, pk=None):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        foodtype = FoodType.objects.get(pk=pk)
        foodtype.label = request.data["foodType"]

        foodtype.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class FoodTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodType
        fields = ('id', 'foodType')