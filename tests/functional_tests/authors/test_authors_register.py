from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from .base_authors import AuthorsFunctionalBaseTest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsFunctionalBaseTest):

    def test_authors_register_form_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(
                form, 'Type your first name'
                )
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field is required', form.text)
        self.form_field_test_with_callback(callback)

    def test_authors_register_form_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(
                form, 'Type your last name'
                )
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field is required', form.text)
        self.form_field_test_with_callback(callback)

    def test_authors_register_form_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(
                form, 'Type your username'
                )
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field is required', form.text)
        self.form_field_test_with_callback(callback)

    def test_authors_register_form_empty_password_error_message(self):
        def callback(form):
            password_field = self.get_by_placeholder(
                form, 'Type your password'
                )
            password_field.send_keys(' ')
            password_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field is required', form.text)
        self.form_field_test_with_callback(callback)
    
    def test_authors_register_form_invalid_email_error_message(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        email_field = self.get_by_placeholder(
            form, 'Type your E-mail'
            )
        email_field.send_keys('rani@rani')
        email_field.send_keys(Keys.ENTER)
        form = self.get_form()
        self.assertIn('Enter a valid email address.', form.text)

    def test_authors_register_form_passwords_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(
                form, 'Type your password'
                )
            password2 = self.get_by_placeholder(
                form, 'Repeat your password'
                )
            password1.send_keys('P@ssW0rd')
            password2.send_keys('P@ssW0rd_Different')

            password2.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('The passwords must be equal!', form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_succesfuly(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        self.get_by_placeholder(form, 'Type your first name').send_keys(
            'First Name'
            )
        self.get_by_placeholder(form, 'Type your last name').send_keys(
            'last Name'
            )
        self.get_by_placeholder(form, 'Type your username').send_keys(
            'MyUsername'
            )
        self.get_by_placeholder(form, 'Type your E-mail').send_keys(
            'rani@rani.com'
            )
        self.get_by_placeholder(form, 'Type your password').send_keys(
            'P@assW0rd'
            )
        self.get_by_placeholder(form, 'Repeat your password').send_keys(
            'P@assW0rd'
            )
        form.submit()
        self.assertIn(
            'User registered with sucess!, Please Log In.',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )
