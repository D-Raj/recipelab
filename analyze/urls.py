from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from analyze.views import *

urlpatterns = patterns('',
    url(r'^$', recipe_page, name='recipe_page'),
    url(r'^(?P<pk>\d+)/$', recipe_page, name='recipe'),
    url(r'^save_recipe/$', save_recipe, name='new_recipe'),
    url(r'^save_recipe/(?P<pk>\d+)/$', save_recipe, name='update_recipe'),
    url(r'^recipe/(?P<pk>\d+)/$', get_recipe, name='get_recipe'),
    url(r'^search_ingredient/$', search_ingredient, name='search_ingredient'),
    url(r'^units/(?P<pk>\d+)/$', get_ingredient_units, name='get_ingredient_units'),
    url(r'^nutrition/$', get_nutrition, name='get_nutrition'),
    url(r'^get_target_category/$', get_target_category, name='get_target_category'),
    url(r'^set_target_category/$', set_target_category, name='set_target_category'),
    url(r'^recipes/$', RecipeList.as_view(), name="recipe_list"),
    url(r'^delete_recipe/(?P<pk>\d+)/$', delete_recipe, name='delete_recipe'),
)
