from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from recipes.tests.test_recipe_base import RecipeMixIn

from .base_recipes import RecipeFunctionalBaseTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTests(RecipeFunctionalBaseTest, RecipeMixIn):

    def test_if_recipe_home_page_with_no_recipe_shows_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here !', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_if_search_for_title_found_the_correct_recipe(self):
        recipes = self.make_recipe_batch()
        title_needed = 'Title needed for the test'
        recipes[0].title = title_needed
        recipes[0].save()

        self.browser.get(self.live_server_url)

        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for recipes"]'
        )
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            title_needed, 
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
            )

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_home_pagination(self):
        self.make_recipe_batch()
        self.browser.get(self.live_server_url)

        pagination = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        pagination.click()
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2
            )
