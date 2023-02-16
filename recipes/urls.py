from django.urls import path

from .views import api, site

app_name = 'recipes'

urlpatterns = [
    path('', site.home, name='home'),
    path('recipe/search/', site.search, name='search'),
    path('recipe/tags/<slug:slug>', site.tag, name='tag'),
    path('recipe/category/<int:category_id>/', site.category, name='category'),  # noqa E501
    path('recipe/<int:id>/', site.recipe, name='recipe'),
    path('recipe/api/v1/', api.recipe_api_list, name='recipe_api_v2'),
    path(
        'recipe/api/v1/<int:pk>/detail', api.recipe_api_detail,
        name='recipe_api_v2_detail'
        ),
    path(
        'recipe/api/v1/tag/<int:pk>/', api.tag_api_detail,
        name='recipe_api_v2_tag'
        )


]
