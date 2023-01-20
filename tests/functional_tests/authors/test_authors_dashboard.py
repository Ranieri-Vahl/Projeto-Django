import pytest
from django.contrib.auth.models import User
from .base_authors import AuthorsFunctionalBaseTest
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsDashboardFunctionalTest(AuthorsFunctionalBaseTest):
    def test_if_user_can_create_a_new_recipe(self):
        self.login()
        self.browser.get(
            self.live_server_url + '/authors/dashboard/recipe/new_recipe'
            )
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[2]/div[1]/form'
            )
        self.fill_form_dummy_data(form)
        self.get_by_name(form, 'preparation_steps').send_keys('TEST IF WRITE SOMETHING') # noqa E501
        self.sleep(20)
