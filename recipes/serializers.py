from rest_framework import serializers

from .models import Tag, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'author',
            'category', 'tags', 'public', 'preparation',
            'tag_objects', 'tag_link'
            ]
    
    public = serializers.BooleanField(source='is_published')
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name'
    )
    category = serializers.StringRelatedField()

    tag_objects = TagSerializer(
        many=True, source='tags'
    )
    tag_link = serializers.HyperlinkedRelatedField(
        source='tags',
        many=True,
        queryset=Tag.objects.all(),
        view_name='recipes:recipe_api_v2_tag'
    )

    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'