from django.urls import path
from api.signin.views import SignInView

urlpatterns = [
    path('', SignInView.as_view(), name = 'signin')
]