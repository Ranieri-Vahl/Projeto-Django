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

    def test_recipe_search_find_recipe_by_title(self):
        title1 = 'Test recipe found title1'
        title2 = 'Test recipe found title2'

        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'}
        )
        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=Test')

        self.assertIn(recipe1, response1.context['recipes']) 
        self.assertIsNot(recipe2, response1.context['recipes'])   
  
        self.assertIn(recipe2, response2.context['recipes']) 
        self.assertIsNot(recipe1, response2.context['recipes'])   

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_recipe_search_find_recipe_by_description(self):
        description1 = 'Test recipe found description1'
        description2 = 'Test recipe found description2'

        recipe1 = self.make_recipe(
            slug='one', description=description1, author_data={
                'username': 'one'
                }
        )
        recipe2 = self.make_recipe(
            slug='two', description=description2, author_data={
                'username': 'two'
                }
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={description1}')
        response2 = self.client.get(f'{search_url}?q={description2}')
        response_both = self.client.get(f'{search_url}?q=Test')
        response1.context

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
