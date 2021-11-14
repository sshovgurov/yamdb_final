from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from rest_framework.serializers import ValidationError


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    CHOICES = (
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    )
    bio = models.TextField(
        max_length=256,
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(max_length=32, choices=CHOICES, default=USER)
    confirmation_code = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=30, unique=True
    )

    class Meta:
        ordering = ('username',)

    def is_admin(self):
        return self.role == self.ADMIN

    def is_moderator(self):
        return self.role == self.MODERATOR

    def is_user(self):
        return self.role == self.USER


class Category(models.Model):
    name = models.TextField(
        'Наименование категории',
        max_length=256,
        help_text='Назовите категорию'
    )
    slug = models.SlugField(
        'Slug',
        max_length=50,
        help_text='Придумайте slug',
        unique=True
    )

    class Meta:
        ordering = ('-name',)
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'],
                name='unique_name_slugg'
            )
        ]

    def __str__(self):
        return f'{self.name[:15]} {self.slug[:15]}'


class Genre(models.Model):
    name = models.CharField(
        'Наименование жанра',
        max_length=256,
        help_text='Назовите жанр'
    )
    slug = models.SlugField(
        'Slug',
        max_length=50,
        help_text='Придумайте slug',
        unique=True
    )

    class Meta:
        ordering = ('-name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'],
                name='unique_name_slug'
            )
        ]

    def __str__(self):
        return f'{self.name[:15]} {self.slug[:15]}'


def current_year_validator(value):
    if value < 1900 or value > timezone.now().year:
        raise ValidationError(
            "Date shouldn't be before 1900 and after current year"
        )
    return value


class Title(models.Model):
    name = models.CharField(
        'Наименование произведения',
        max_length=256,
        help_text='Наименование'
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[current_year_validator]
    )
    description = models.TextField(
        'Описание произведения',
        max_length=2000,
        help_text='Опишите произведение',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return f'{self.name[:15]}({self.year}) {self.genre.name}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveIntegerField(
        'Оценка произведения',
        validators=(
            MinValueValidator(1, message='Не меньше 1'),
            MaxValueValidator(10, message='Не больше 10')
        )
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-title',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'
            )
        ]

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'Комментарий от {self.author} к {self.review_id}'
