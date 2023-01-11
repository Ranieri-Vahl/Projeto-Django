from .base_authors import AuthorsFunctionalBaseTest
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsFunctionalBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'P@ssW0rd'
        user = User.objects.create_user(
            username='my_user', password=string_password
        )
        self.browser.get(self.live_server_url + '/authors/login/')
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys(user.username)
        password_field.send_keys(string_password)
        form.submit()

        self.assertIn(
            f'You are logged in with {user.username}',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )
    
    def test_raises_error_404_if_request_is_not_post(self):
        self.browser.get(self.live_server_url + '/login/create/')
        self.assertIn(
            'Not Found', self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_raises_message_error_if_form_is_not_valid(self):
        self.browser.get(self.live_server_url + '/authors/login/')
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys('   ')
        password_field.send_keys('   ')
        form.submit()
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )

    def test_raises_message_error_if_user_is_not_authenticated(self):
        self.browser.get(self.live_server_url + '/authors/login/')
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys('usertest')
        password_field.send_keys('passtest')
        form.submit()
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )
