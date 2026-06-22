from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTH = 256
MAX_LENGTH_SLUG = 50
NAME_LENGTH = 30


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'User'
        MODERATOR = 'moderator', 'Moderator'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(
        unique=True,
        max_length=settings.EMAIL_MAX_LENGTH,
        verbose_name='Email',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    role = models.CharField(
        max_length=NAME_LENGTH,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль',
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self):
        return (
            self.role == self.Role.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username


class NameSlugModel(models.Model):
    name = models.CharField(max_length=MAX_LENGTH,
                            verbose_name='Наименование')
    slug = models.SlugField(max_length=MAX_LENGTH_SLUG,
                            unique=True,
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
        default='')
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


# Заглушка для проверки импорта Review из csv
class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)


# Заглушка для проверки импорта Comment из csv
class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
