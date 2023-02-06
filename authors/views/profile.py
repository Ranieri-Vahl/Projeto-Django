import os

from django.shortcuts import get_object_or_404, render

from authors.models import Profile
from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = os.environ.get('PER_PAGE')


def ProfileView(request, id):
    profile = get_object_or_404(Profile.objects.filter(
        pk=id
    ).select_related('author'), pk=id)

    recipes = Recipe.objects.filter(
        is_published=True, author=profile.author,
    ).order_by('-id')

    paje_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE,
        )

    return render(request, 'authors/pages/profile.html', context={
        'profile': profile,
        'recipes': paje_obj,
        'pagination_range': pagination_range,
    })