from rest_framework import serializers

from .models import Recipe, Tag


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
            'tag_objects', 'tag_link', 'preparation_time', 
            'preparation_time_unit', 'servings', 'servings_unit',
            'preparation_steps'
            ]
    
    public = serializers.BooleanField(
        source='is_published',
        read_only=True,
        )
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name',
        read_only=True,
    )
    category = serializers.StringRelatedField(
        read_only=True,
    )

    tag_objects = TagSerializer(
        many=True, 
        source='tags',
        read_only=True,
    )
    tag_link = serializers.HyperlinkedRelatedField(
        source='tags',
        many=True,
        view_name='recipes:recipe_api_v2_tag',
        read_only=True,
    )

    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        if self.instance is not None and attrs.get('title') is None:
            attrs['title'] = self.instance.title

        if self.instance is not None and attrs.get('description') is None:
            attrs['description'] = self.instance.description

        title = attrs.get('title')
        description = attrs.get('description')

        if len(title) < 5:
            raise serializers.ValidationError(
                'The title must have at least 5 characters'
                )

        if description == title:
            raise serializers.ValidationError({
                "title": ["The title cannot be equal to description"],
                "description": ["The description cannot be equal to title"],
                })

        super_clean = super().validate(attrs)
        return super_clean

            