from django.contrib import admin

from reviews.models import Categories, Genres, Titles


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
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


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
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


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
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
