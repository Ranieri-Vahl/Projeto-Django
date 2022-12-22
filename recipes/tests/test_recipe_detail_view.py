from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailTest(RecipeTestBase):
    def test_function_detail_view_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_status_code_is_200_OK(self):
        self.make_recipe()
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': 1})
            )
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': 1000})
            )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_recipes(self):
        needed_title = 'This is a detail page test that loads one recipe'
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        self.assertIn(
            'This is a detail page test that loads one recipe', content
            )

    def test_recipe_detail_dont_show_recipe_if_is_published_false(self): # noqa E508
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': recipe.id})
            )
        self.assertEqual(response.status_code, 404)

    