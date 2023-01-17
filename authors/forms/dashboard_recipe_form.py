from django import forms

from recipes.models import Recipe
from utils.django_forms import add_attr


class AuthorsRecipeForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
    
    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('servings', 'Servings'),
                    ('cups', 'Cup(s)'),
                    ('slices', 'Slice(s)'),
                    ('piece', 'Piece(s)'),

                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('minutes', 'Minutes'),
                    ('hours', 'Hours'),
                )
            )
        }
