from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

urlpatterns = [
    path('', TokenRefreshView.as_view(), name = 'token_refresh')
]