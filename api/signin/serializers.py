from rest_framework import serializers
from api.backends import EmailAuthenticationBackend

# Created a Sign In Serializer to access json data send by POST Request
# Modified default validate because we want to validate with email
class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = EmailAuthenticationBackend.authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        attrs['user'] = user
        return attrs