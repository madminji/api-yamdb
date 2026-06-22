from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from reviews.models import Category, Genre, Title, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        'role',
        'is_staff',
        'is_superuser',
    )
    search_fields = (
        'username',
        'email',
    )
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('bio', 'role')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('email', 'bio', 'role')}),
    )


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
