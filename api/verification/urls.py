from django.urls import path
from .views import TokenAuthenticationView

urlpatterns = [
    path('', TokenAuthenticationView.as_view(), name = 'verify')
]