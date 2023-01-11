from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):

    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='usertest', password='passtest')
        self.client.login(username='usertest', password='passtest')
     
        response = self.client.get(reverse('authors:logout'), follow=True)
        self.assertIn('Invalid logout', response.content.decode('utf-8'))
       
    def test_user_tries_to_logout_using_another_username(self):
        User.objects.create_user(username='usertest', password='passtest')
        self.client.login(username='usertest', password='passtest')

        response = self.client.post(
            reverse('authors:logout'), data={
                'username': 'anotherusertest'
            }, follow=True
            )
        self.assertIn('Invalid logout user', response.content.decode('utf-8'))

    def test_user_can_logout_sucessfully(self):
        User.objects.create_user(username='usertest', password='passtest')
        self.client.login(username='usertest', password='passtest')
        
        response = self.client.post(
            reverse('authors:logout'), data={
                'username': 'usertest'
            }, follow=True
            )
        self.assertIn(
            'Logged out successfully', response.content.decode('utf-8')
            )

