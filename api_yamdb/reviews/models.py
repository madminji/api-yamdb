from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
MAX_LENGTH = 256
NAME_LENGTH = 30


class NameSlugModel(models.Model):
    name = models.CharField(max_length=MAX_LENGTH,
                            verbose_name='Наименование')
    slug = models.SlugField(unique=True,
                            verbose_name='Идентификатор')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:NAME_LENGTH]


class Category(NameSlugModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Наименование')
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,)
    year = models.IntegerField(verbose_name='Год выхода')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:NAME_LENGTH]
