from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from users.views import (get_phone_view, create_user, UserAPIView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/get_phone/', get_phone_view, name='get_phone_number'),
    path('api/auth/create_user/', create_user, name='create_user'),
    path('api/profile/', UserAPIView.as_view()),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularRedocView.as_view(url_name='schema'), name='docs'),
]
