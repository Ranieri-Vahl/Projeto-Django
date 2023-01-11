import time

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