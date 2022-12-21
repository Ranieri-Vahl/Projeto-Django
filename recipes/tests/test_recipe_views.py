from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
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
        self.assertIn('<h1>No recipes found here !</h1>', response.content.decode('utf-8')) # noqa E508

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        context = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(context), 1)

    def test_recipe_home_dont_show_recipes_if_is_published_false(self): # noqa E508
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('<h1>No recipes found here !</h1>', content)

    def test_function_category_view_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_status_code_is_200_OK(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1})) # noqa E508
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000})) # noqa E508
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category page test'
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn('This is a category page test', content)

    def test_recipe_category_dont_show_recipes_if_is_published_false(self): # noqa E508
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:category', kwargs={'category_id': recipe.category.id})) # noqa E508
        self.assertEqual(response.status_code, 404)

    def test_function_detail_view_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_status_code_is_200_OK(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1})) # noqa E508
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000})) # noqa E508
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_recipes(self):
        needed_title = 'This is a detail page test that loads one recipe'
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        self.assertIn('This is a detail page test that loads one recipe', content) # noqa E508

    def test_recipe_detail_dont_show_recipe_if_is_published_false(self): # noqa E508
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': recipe.id})) # noqa E508
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_uses_the_correct_view(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertEqual(resolved.func, views.search)

    def test_recipe_search_loads_the_correct_template(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')