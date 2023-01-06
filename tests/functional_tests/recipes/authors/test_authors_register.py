from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base_authors import AuthorsFunctionalBaseTest


class AuthorsRegisterTest(AuthorsFunctionalBaseTest):

    def test_authors_register_form_empty_first_name_error_message(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
            )

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys("dummy@dummy.com")

        first_name_field = self.get_by_placeholder(
            form, 'Type your first name'
            )
        first_name_field.send_keys(' ')
        first_name_field.send_keys(Keys.ENTER)

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
            )
        self.assertIn('This field is required', form.text)
