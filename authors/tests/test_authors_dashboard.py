from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from authors import views
from recipes.tests.test_recipe_base import RecipeMixIn


class AuthorsDashboardTest(TestCase, RecipeMixIn):

    def test_if_url_go_to_correct_view(self):
        url = resolve(reverse('authors:dashboard'))
        self.assertIs(url.func, views.dashboard)

    def test_if_view_render_the_correct_template(self):
        User.objects.create_user(username='usertest', password='passtest')
        self.client.login(username='usertest', password='passtest')

        response = self.client.get(reverse('authors:dashboard'))
        self.assertTemplateUsed(response, 'authors/pages/dashboard.html')
    
    def test_if_dasboard_page_is_login_required(self):
        response = self.client.get(reverse('authors:dashboard'))
        self.assertTemplateNotUsed(response, 'authors/pages/dashboard.html')

    def test_dashboard_home_template_shows_no_recipe_found_if_no_recipe(self):
        User.objects.create_user(username='usertest', password='passtest')
        self.client.login(username='usertest', password='passtest')
        
        response = self.client.get(reverse('authors:dashboard'))
        self.assertIn(
            '<h2>No recipes found here !</h2>',
            response.content.decode('utf-8')
            )
    
    def test_if_dashboard_home_shows_the_correct_user_in_title(self):
        username = 'usertest'
        User.objects.create_user(username=username, password='passtest')
        self.client.login(username='usertest', password='passtest')
        
        response = self.client.get(reverse('authors:dashboard'))
        self.assertIn(
            f'Dashboard ({username})',
            response.content.decode('utf-8')
            )
''' # noqa
    def test_if_dashboard_home_shows_recipes(self):
        title1 = 'titletest'
        User.objects.create_user(username='usertest', password='passtest')
        self.client.login(username='usertest', password='passtest')

        self.make_recipe(
            slug='one', title=title1, author_data={'username': 'usertest'}, 
            is_published=False
            )
        
        response = self.client.get(reverse('authors:dashboard'))
        content = response.content.decode('utf-8')
        context = response.context['recipes']
        self.assertIn(title1, content)
        self.assertEqual(len(context), 1)
'''