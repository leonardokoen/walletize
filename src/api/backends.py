from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model



#Created my own backend authentication because we want
# to log in eith email instead of username

class EmailAuthenticationBackend(ModelBackend):
    def authenticate(email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None