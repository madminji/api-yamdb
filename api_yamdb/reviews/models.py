from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


MAX_LENGTH = 256
MAX_LENGTH_SLUG = 50
NAME_LENGTH = 30
ROLE_MAX_LENGTH = 20


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

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
        max_length=ROLE_MAX_LENGTH,
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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField('Текст отзыва')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        choices=[(i, str(i)) for i in range(1, 11)]  # от 1 до 10
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.author} - {self.title} - {self.score}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author} - {self.review}'
