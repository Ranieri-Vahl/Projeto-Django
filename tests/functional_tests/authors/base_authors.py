import time

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By

from utils.browser import make_chrome_browser


class AuthorsFunctionalBaseTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=10):
        time.sleep(seconds)

    def get_by_placeholder(self, webelement, placeholder):
        return webelement.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
            )

    def get_by_name(self, webelement, name):
        return webelement.find_element(
            By.NAME, f'"{name}"'
            )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
            )    

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys("dummy@dummy.com")    

        callback(form)
        return form

    def login(self):
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
