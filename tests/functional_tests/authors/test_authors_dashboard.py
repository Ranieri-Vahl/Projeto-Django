import os

import pytest
from selenium.webdriver.common.by import By

from .base_authors import AuthorsFunctionalBaseTest


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
        form.find_element(By.NAME, 'title').send_keys('TESTING')
        form.find_element(By.NAME, 'description').send_keys('TEST')
        form.find_element(By.NAME, 'preparation_time').send_keys('2')
        form.find_element(By.NAME, 'servings').send_keys('3')
        form.find_element(By.NAME, 'preparation_steps').send_keys('TEST')
        form.find_element(By.ID, 'id_cover').send_keys(
            os.getcwd()+"/tests/functional_tests/images_test/image.png"
            ) 
        form.submit()
        self.assertIn(
            'Your recipe was save with success',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )


    def test_form_raises_error_if_title_less_than_5_chars_and_equal_to_description(self): # noqa E501
        self.login()
        self.browser.get(
            self.live_server_url + '/authors/dashboard/recipe/new_recipe'
            )
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[2]/div[1]/form'
            )
        form.find_element(By.NAME, 'title').send_keys('TEST')
        form.find_element(By.NAME, 'description').send_keys('TEST')
        form.find_element(By.NAME, 'preparation_time').send_keys('2')
        form.find_element(By.NAME, 'servings').send_keys('3')
        form.find_element(By.NAME, 'preparation_steps').send_keys('TEST')
        form.find_element(By.ID, 'id_cover').send_keys(
            os.getcwd()+"/tests/functional_tests/images_test/image.png"
            ) 
        form.submit()
        self.assertIn(
            'The title must have at least 5 characters',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )
        self.assertIn(
            'The title cannot be equal to description',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )

    def test_if_user_can_see_your_recipes(self):
        self.login()
        self.browser.get(
            self.live_server_url + '/authors/dashboard/recipe/new_recipe'
            )
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[2]/div[1]/form'
            )
        form.find_element(By.NAME, 'title').send_keys('TESTING')
        form.find_element(By.NAME, 'description').send_keys('TEST')
        form.find_element(By.NAME, 'preparation_time').send_keys('2')
        form.find_element(By.NAME, 'servings').send_keys('3')
        form.find_element(By.NAME, 'preparation_steps').send_keys('TEST')
        form.find_element(By.ID, 'id_cover').send_keys(
            os.getcwd()+"/tests/functional_tests/images_test/image.png"
            ) 
        form.submit()
        self.browser.get(
            self.live_server_url + '/authors/dashboard/'
            )
        self.assertIn(
            'TESTING',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )

    def test_if_user_can_delete_your_recipes(self):
        self.login()
        self.browser.get(
            self.live_server_url + '/authors/dashboard/recipe/new_recipe'
            )
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[2]/div[1]/form'
            )
        form.find_element(By.NAME, 'title').send_keys('TESTING')
        form.find_element(By.NAME, 'description').send_keys('TEST')
        form.find_element(By.NAME, 'preparation_time').send_keys('2')
        form.find_element(By.NAME, 'servings').send_keys('3')
        form.find_element(By.NAME, 'preparation_steps').send_keys('TEST')
        form.find_element(By.ID, 'id_cover').send_keys(
            os.getcwd()+"/tests/functional_tests/images_test/image.png"
            ) 
        form.submit()
        self.browser.get(
            self.live_server_url + '/authors/dashboard/'
            )
        remove_button = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[2]/ul/li/form/button'
            )
        remove_button.click()
        self.assertIn(
            'Recipe deleted with success',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )

    def test_if_user_can_edit_your_recipes(self):
        self.login()
        self.browser.get(
            self.live_server_url + '/authors/dashboard/recipe/new_recipe'
            )
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[2]/div[1]/form'
            )
        form.find_element(By.NAME, 'title').send_keys('TESTING')
        form.find_element(By.NAME, 'description').send_keys('TEST')
        form.find_element(By.NAME, 'preparation_time').send_keys('2')
        form.find_element(By.NAME, 'servings').send_keys('3')
        form.find_element(By.NAME, 'preparation_steps').send_keys('TEST')
        form.find_element(By.ID, 'id_cover').send_keys(
            os.getcwd()+"/tests/functional_tests/images_test/image.png"
            ) 
        form.submit()
        self.browser.get(
            self.live_server_url + '/authors/dashboard/'
            )
        recipe = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[2]/ul/li/a'
            )
        recipe.click()
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[2]/div[1]/form'
            )
        form.find_element(By.NAME, 'title').send_keys('EDITED')
        form.submit()
        self.assertIn(
            'Your recipe was save with success',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )
