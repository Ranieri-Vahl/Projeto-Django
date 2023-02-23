from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Recipe, Tag
from ..serializers import RecipeSerializer, TagSerializer


class RecipeAPIv1List(APIView):
    def get(self, request):
        recipes = Recipe.objects.filter(
            is_published=True 
            ).order_by(
                '-id'
                ).select_related('author', 'category').prefetch_related(
                    'tags'
                    )[:10]
        serializer = RecipeSerializer(
            instance=recipes, many=True, context={'request': request}
            )
        return Response(serializer.data)

    def post(self, request):
        serializer = RecipeSerializer(
            data=request.data
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )                


class RecipeAPIv1Detail(APIView):
    def get_recipe(self, pk):
        recipe = get_object_or_404(Recipe.objects.filter(
            is_published=True, pk=pk,
            ).select_related('author', 'category').prefetch_related(
                    'tags'
                    ))
        return recipe

    def get(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe, many=False, context={'request': request}
            )
        return Response(serializer.data)

    def patch(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.filter(pk=pk))
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)