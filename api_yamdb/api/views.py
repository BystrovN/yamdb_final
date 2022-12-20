from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from . import serializers
from .rating import Rating
from .filters import TitleFilter
from reviews.models import Category, Genre, Title, Review, Comment
from users.permissions import IsAdmin, AdminOrReadOnly, AuthorOrAdminOrReadOnly
from .pagination import CustomPagination


User = get_user_model()


class CategoryListCreateView(ListCreateAPIView):
    """Представление для просмотра и создания записи в модели категорий."""

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = CustomPagination


class CategoryDeleteView(APIView):
    """Представление для удаления записи из модели категорий."""

    permission_classes = (IsAdmin,)
    serializer_class = serializers.CategorySerializer

    def delete(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        category.delete()

        msg = f'Категория "{category.name}" удалена'
        return Response(
            {'message': msg},
            status=status.HTTP_204_NO_CONTENT,
        )


class GenreListCreateView(ListCreateAPIView):
    """Представление для просмотра и создания записи в модели жанров."""

    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = CustomPagination


class GenreDeleteView(APIView):
    """Представление для удаления записи из модели жанров."""

    permission_classes = (IsAdmin,)
    serializer_class = serializers.GenreSerializer

    def delete(self, request, slug):
        genre = get_object_or_404(Genre, slug=slug)
        genre.delete()

        msg = f'Жанр "{genre.name}" удален'
        return Response(
            {'message': msg},
            status=status.HTTP_204_NO_CONTENT,
        )


class TitleListCreateView(ListCreateAPIView):
    """Представление для просмотра и создания записи в модели произведений."""

    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleSerializerRead

        return serializers.TitleSerializerWrite


class TitleEditView(APIView):
    """
    Представление для редактирования и удаления записи из модели произведений.
    """

    permission_classes = (AdminOrReadOnly,)

    def get_title(self, titles_id):
        return get_object_or_404(Title, id=titles_id)

    def get(self, request, titles_id):
        title = self.get_title(titles_id)
        serializer = serializers.TitleSerializerRead(title)
        return Response(serializer.data)

    def patch(self, request, titles_id):
        title = self.get_title(titles_id)
        serializer = serializers.TitleSerializerWrite(
            title, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, titles_id):
        title = self.get_title(titles_id)
        title.delete()

        msg = f'Произведение "{title.name}" удалено'
        return Response(
            {'message': msg},
            status=status.HTTP_204_NO_CONTENT,
        )


class ReviewListCreateView(ListCreateAPIView):
    """Представление для просмотра и создания записи в модели отзывов."""

    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('titles_id'))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()

        if Review.objects.filter(
            title=title, author=self.request.user
        ).exists():
            raise ValidationError(
                'Пользователь может оставить только '
                'один отзыв на произведение'
            )

        serializer.save(author=self.request.user, title=title)
        Rating.title_rating(self.kwargs.get('titles_id'))


class ReviewEditView(APIView):
    """
    Представление для редактирования и удаления записи из модели отзывов.
    """

    permission_classes = (AuthorOrAdminOrReadOnly,)
    serializer_class = serializers.ReviewSerializer

    def get_review(self, titles_id, review_id):
        review = get_object_or_404(Review, id=review_id)
        if review.title.id != titles_id:
            raise NotFound()

        self.check_object_permissions(self.request, review)
        return review

    def get(self, request, titles_id, review_id):
        review = self.get_review(titles_id, review_id)
        serializer = self.serializer_class(review)
        return Response(serializer.data)

    def patch(self, request, titles_id, review_id):
        review = self.get_review(titles_id, review_id)
        serializer = self.serializer_class(
            review, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            if request.data.get('score'):
                Rating.title_rating(titles_id)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, titles_id, review_id):
        review = self.get_review(titles_id, review_id)
        review.delete()
        Rating.title_rating(titles_id)

        msg = f'Отзыв на произведение "{review.title.name}" удален'
        return Response(
            {'message': msg},
            status=status.HTTP_204_NO_CONTENT,
        )


class CommentListCreateView(ListCreateAPIView):
    """Представление для просмотра и создания записи в модели комментариев."""

    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination

    def get_review(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        if review.title.id != self.kwargs.get('titles_id'):
            raise NotFound()

        return review

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()

        serializer.save(author=self.request.user, review=review)


class CommentListEditView(APIView):
    """
    Представление для редактирования и удаления записи из модели комментариев.
    """

    permission_classes = (AuthorOrAdminOrReadOnly,)
    serializer_class = serializers.CommentSerializer

    def get_comment(self, titles_id, review_id, comment_id):
        review = get_object_or_404(Review, id=review_id)
        comment = get_object_or_404(Comment, id=comment_id)

        if review.title.id != titles_id or comment.review.id != review_id:
            raise NotFound()

        self.check_object_permissions(self.request, comment)
        return comment

    def get(self, request, titles_id, review_id, comment_id):
        comment = self.get_comment(titles_id, review_id, comment_id)
        serializer = self.serializer_class(comment)
        return Response(serializer.data)

    def patch(self, request, titles_id, review_id, comment_id):
        comment = self.get_comment(titles_id, review_id, comment_id)
        serializer = self.serializer_class(
            comment, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, titles_id, review_id, comment_id):
        comment = self.get_comment(titles_id, review_id, comment_id)
        comment.delete()

        msg = (
            'Комментарий к отзыву на произведение'
            f' "{comment.review.title.name}" удален'
        )
        return Response(
            {'message': msg},
            status=status.HTTP_204_NO_CONTENT,
        )
