from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserView.as_view()),
    path('me/', views.UserMeView.as_view()),
    path('signup/', views.NewUserView.as_view()),
    path('token/', views.JWTUserView.as_view()),
    path('<str:username>/', views.UserDetailView.as_view()),
]
