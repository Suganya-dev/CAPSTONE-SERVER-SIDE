from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from Eventplannerapi.models import Category

class CategoriesView(ViewSet):

    # Create a new Python instance of the Category class
    # and set its properties from what was sent in the
    # body of the request from the client.
    def create(self, request):
        category = Category()

        category.label = request.data["label"]
 
   # Use the Django ORM to get the record from the database
        try:
            category.save()
            serializer = CategorySerializer(
                category, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    # This method will handle request for a single category
    # Handle GET requests for single category

    def retrieve(self, request, pk=None):

        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(
                category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    # Get all category records from the database
    def list(self, request):

        categories = Category.objects.all()

        ordered_posts = categories.order_by('label')

        serializer = CategorySerializer(
            ordered_posts, many=True, context={'request': request})
        return Response(serializer.data)

    # This will handle the edit of a category

    def update(self, request, pk=None):
        """Handle PUT requests for a category
        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of category, get the category record
        # from the database whose primary key is `pk`
        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]

        category.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    #  Handle DELETE requests for a single category
    def destroy(self, request, pk=None):

        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'label')
