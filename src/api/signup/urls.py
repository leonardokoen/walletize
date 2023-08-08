from django.urls import path
from api.signup.views import SignUpView


urlpatterns = [
    path('', SignUpView.as_view(), name = 'signup')
]