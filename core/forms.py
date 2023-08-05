from .models import User, CustomUserManager
from django.contrib.auth.forms import UserCreationForm
from django import forms




class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=240)
    last_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=50)
    vat_number = forms.CharField(max_length=15)
    date_of_birth = forms.DateField()

    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number', 'vat_number', 'date_of_birth', 'email'] 