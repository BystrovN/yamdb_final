from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_title_year

User = get_user_model()
SLICE_TEXT_STOP: int = 20


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(validators=(validate_title_year,))
    rating = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'жанр к произведению'
        verbose_name_plural = 'жанры к произведениям'

    def __str__(self):
        return self.title.name + ' -> ' + self.genre.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1, 'Оценка не может быть меньше одного балла'),
            MaxValueValidator(10, 'Оценка не может быть больше десяти баллов'),
        )
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_related_name = 'reviews'
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'), name='title_author'
            )
        ]

    def __str__(self):
        return self.text[:SLICE_TEXT_STOP]


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ('-id',)

    def __str__(self):
        return self.text[:SLICE_TEXT_STOP]
