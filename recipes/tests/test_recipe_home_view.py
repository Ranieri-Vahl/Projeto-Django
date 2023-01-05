from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

from unittest.mock import patch


class RecipeHomeView(RecipeTestBase):
    def test_function_home_view_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_status_code_is_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_load_template_is_corrected(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipe_found_if_no_recipe(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here !</h1>',
            response.content.decode('utf-8')
            )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        context = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(context), 1)

    def test_recipe_home_dont_show_recipes_if_is_published_false(self): # noqa E501
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('<h1>No recipes found here !</h1>', content)

    def test_recipe_home_loads_correct_paginated(self):
        self.make_recipe_batch(10)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            context = response.context['recipes']
            paginator = context.paginator
            objects = len(context.object_list)

            self.assertEqual(objects, 3)
            self.assertEqual(paginator.num_pages, 4)

    def test_if_invalid_page_query_uses_page_one(self):
        self.make_recipe_batch(10)
        
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=12ab')
            self.assertEqual(response.context['recipes'].number, 1)

            response = self.client.get(reverse('recipes:home') + '?page=3')
            self.assertEqual(response.context['recipes'].number, 3)

