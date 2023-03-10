from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='api/redoc.html'),
        name='redoc',
    ),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/', include('api.urls')),
]
