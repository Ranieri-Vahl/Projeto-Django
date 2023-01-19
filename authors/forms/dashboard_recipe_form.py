from collections import defaultdict

from django import forms
from django.forms import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr, is_positive_number


class AuthorsRecipeForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)
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

    def clean(self):
        super_clean = super().clean()
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')

        if len(title) < 5:
            self._my_errors['title'].append(
                'The title must have at least 5 characters'
                )

        if description == title:
            self._my_errors['title'].append(
                'The title cannot be equal to description'
                )
            self._my_errors['description'].append(
                'The description cannot be equal to title'
                )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number')

        return field_value

