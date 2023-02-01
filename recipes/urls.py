from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/search/', views.search, name='search'),
    path('recipe/tags/<slug:slug>', views.tag, name='tag'),
    path('recipe/category/<int:category_id>/', views.category, name='category'),  # noqa E501
    path('recipe/<int:id>/', views.recipe, name='recipe'),
]
