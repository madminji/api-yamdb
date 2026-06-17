from django.contrib import admin

from reviews.models import Category, Genre, Title


class NameSlugAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    list_editable = (
        'slug',
    )
    search_fields = (
        'name',
        'slug'
    )
    list_filter = (
        'name',
        'slug'
    )
    list_display_links = ('name',)


@admin.register(Category)
class CategoryAdmin(NameSlugAdmin):
    ...


@admin.register(Genre)
class GenreAdmin(NameSlugAdmin):
    ...


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category'
    )
    list_editable = (
        'year',
        'category'
    )
    search_fields = (
        'name',
        'year',
        'category'
    )
    list_filter = (
        'name',
        'year',
        'category'
    )
    list_display_links = ('name',)
