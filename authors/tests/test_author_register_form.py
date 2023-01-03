from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterForm(TestCase):
    @parameterized.expand([
        ('first_name', 'Type your first name'),
        ('last_name', 'Type your last name'),
        ('username', 'Type your username'),
        ('email', 'Type your E-mail'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_placeholder_of_fields_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder'] # noqa E501
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Confirm password'),
    ])
    def test_labels_of_fields_is_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(current_label, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self):
        self.form_data = {
            'username': 'Username53',
            'first_name': 'First',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': '@Str0ngPassword1',
            'password2': '@Str0ngPassword1',
        }
        return super().setUp()

    @parameterized.expand([
        ('username', 'This field is required'),
        ('first_name', 'This field is required'),
        ('last_name', 'This field is required'),
        ('email', 'This field is required'),
        ('password', 'This field is required'),
        ('password2', 'This field is required'),

    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
   
    def test_username_field_min_lenght_should_be_5(self):
        self.form_data['username'] = 'joao'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Min 5 and max 20 characters. Letters, numbers and @/./+/-/_ only' # noqa E501
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_max_lenght_should_be_20(self):
        self.form_data['username'] = 'a' * 21  
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Min 5 and max 20 characters. Letters, numbers and @/./+/-/_ only' # noqa E501
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_has_upper_lower_numbers_and_special_characters(self):
        self.form_data['password'] = 'abc123' 
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Must have 1 upper case letter, 1 lower case letter, 1 number and min 8 characters'   # noqa E501
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@ABCabc123' 
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_password_and_password2_are_equal(self):
        self.form_data['password'] = '@ABCabc123'
        self.form_data['password2'] = 'ABCabc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'The passwords must be equal!' 
        self.assertIn(msg, response.content.decode('utf-8'))  

        self.form_data['password'] = '@ABCabc123'
        self.form_data['password2'] = '@ABCabc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_if_not_method_post_raises_404(self): 
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_if_email_is_already_registered(self):
        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'This email is already registered'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_if_author_can_login(self):
        url = reverse('authors:create')
        self.form_data.update({
            'username': 'testuser',
            'password': '@ABCabc123',
            'password2': '@ABCabc123',
        })
        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='@ABCabc123',          
        )

        self.assertTrue(is_authenticated)

