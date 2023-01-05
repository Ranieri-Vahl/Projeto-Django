import pytest
from selenium.webdriver.common.by import By

from recipes.tests.test_recipe_base import RecipeMixIn

from .base import RecipeFunctionalBaseTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTests(RecipeFunctionalBaseTest, RecipeMixIn):

    def test_if_recipe_home_page_with_no_recipe_shows_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here !', body.text)
