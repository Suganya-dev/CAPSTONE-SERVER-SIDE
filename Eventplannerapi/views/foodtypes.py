from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from Eventplannerapi.models import FoodType

class FoodtypesView(ViewSet):

    def create(self, request):
        
        foodtype = FoodType()
        foodtype.label = request.data["label"]
        try:
            foodtype.save()
            serializer = FoodTypeSerializer(foodtype, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

            # this will handle request for a single foodtype

    def retrieve(self, request, pk=None):

        try:
            foodtype = FoodType.objects.get(pk=pk)
            serializer = FoodTypeSerializer(foodtype, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        foodtype = FoodType.objects.all()

        # ordered_foodtypes = foodtype.order_by("label")

        serializer = FoodTypeSerializer(foodtype, many=True, context={'request': request})
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
        foodtype.label = request.data["label"]

        foodtype.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            foodtype = FoodType.objects.get(pk=pk)
            foodtype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except FoodType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FoodTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodType
        fields = ('id', 'label')
