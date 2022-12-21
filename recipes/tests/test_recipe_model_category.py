from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class CategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(name='Category Testing')
        return super().setUp()
    
    def test_category_model_str_representation(self):
        self.assertEqual(str(self.category), self.category.name)
    
    def test_category_model_if_maxlength_of_namefield_is_bigger_than_65_chars(self): # noqa E508
        self.category.name = 'a' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
