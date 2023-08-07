from rest_framework import serializers


class ActivationSerializer(serializers.Serializer):
    token = serializers.CharField()
    id_front = serializers.ImageField()
    id_back = serializers.ImageField()
    selfie = serializers.ImageField()