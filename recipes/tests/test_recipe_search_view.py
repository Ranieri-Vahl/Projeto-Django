from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchView(RecipeTestBase):
    def test_recipe_search_uses_the_correct_view(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertEqual(resolved.func, views.search)

    def test_recipe_search_loads_the_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertTemplateUsed(response, 'recipes/pages/search-page.html')

    def test_recipe_search_raises_404_if_not_found(self):   
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_if_the_title_is_escaped_and_on_page(self):
        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertIn(
            'Search for &quot;test&quot;', 
            response.content.decode('utf-8')
            )
