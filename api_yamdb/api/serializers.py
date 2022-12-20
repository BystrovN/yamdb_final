from rest_framework import serializers
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер модели категорий."""

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер модели жанров."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializerRead(serializers.ModelSerializer):
    """Сериалайзер для чтения из модели произведений."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class TitleSerializerWrite(serializers.ModelSerializer):
    """Сериалайзер для записи в модель произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер модели отзывов."""

    author = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        read_only_fields = ('author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер модели комментариев."""

    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = ('author', 'pub_date')
