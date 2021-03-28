from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .models import Category, Comment, CustomUser, Genre, Review, Title

model = Review, Comment, Title, Category, Genre, CustomUser
models = apps.get_models(model)

try:
    for mod in model:
        admin.site.register(mod)
except AlreadyRegistered:
    pass


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'title', 'pub_date')


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('category', 'year')
    empty_value_display = '-пусто-'


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('review', 'text')


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('id',)
    empty_value_display = '-пусто-'


class GenresAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('id',)
    empty_value_display = '-пусто-'
