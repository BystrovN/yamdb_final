from django.urls import path

from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view()),
    path('categories/<slug:slug>/', views.CategoryDeleteView.as_view()),
    path('genres/', views.GenreListCreateView.as_view()),
    path('genres/<slug:slug>/', views.GenreDeleteView.as_view()),
    path('titles/', views.TitleListCreateView.as_view()),
    path('titles/<int:titles_id>/', views.TitleEditView.as_view()),
    path(
        'titles/<int:titles_id>/reviews/',
        views.ReviewListCreateView.as_view(),
    ),
    path(
        'titles/<int:titles_id>/reviews/<int:review_id>/',
        views.ReviewEditView.as_view(),
    ),
    path(
        'titles/<int:titles_id>/reviews/<int:review_id>/comments/',
        views.CommentListCreateView.as_view(),
    ),
    path(
        (
            'titles/<int:titles_id>/reviews/<int:review_id>/'
            'comments/<int:comment_id>/'
        ),
        views.CommentListEditView.as_view(),
    ),
]
