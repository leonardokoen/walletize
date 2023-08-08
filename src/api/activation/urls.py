from django.urls import path
from .views import UserActivationView

urlpatterns = [
    path('', UserActivationView.as_view(), name = 'activate')
]