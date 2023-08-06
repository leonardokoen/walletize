from rest_framework import serializers
from api.models import User
from django.contrib.auth.hashers import make_password

# Created a Sign Up Serializer to access json data send by POST Request
# Modified default create because I wanted to hash the password
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'vat_number', 'date_of_birth', 'phone_number', 'email', 'password']