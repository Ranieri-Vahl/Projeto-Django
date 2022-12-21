from django.core.exceptions import ValidationError

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
  
    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='test field default'),
            author=self.make_author(username='test field default author'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug1',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            cover='https://loremflickr.com/320/240?random',
        )
        recipe.full_clean()
        recipe.save()

        return recipe

    def test_recipe_fields_max_length(self):
        fields = [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ]

        for field, max_length in fields:
            with self.subTest(field=field, max_length=max_length):
                setattr(self.recipe, field, 'a' * (max_length + 1))
                with self.assertRaises(ValidationError):
                    self.recipe.full_clean()

    def test_field_preparation_steps_is_html__isfalse_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html)
                       
    def test_field_is_published__isfalse_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published)

    def test_recipe_model_str_representation(self):
        self.recipe.title = 'Testing str Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing str Representation')