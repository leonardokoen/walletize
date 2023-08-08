from rest_framework import serializers
# from api.models import ActivationImage
from django.core.files.storage import default_storage
import uuid
import os
# class TokenSerializer(serializers.Serializer):
#     pass


class ActivationSerializer(serializers.Serializer):

    token = serializers.CharField()
    id_front = serializers.ImageField()
    id_back = serializers.ImageField()
    selfie = serializers.ImageField()
    
    
    def create(self, validated_data):
        # Save the file to a local folder instead of the database

        id_front = validated_data.pop('id_front')
        id_front_name = self.generate_filename(id_front.name)
        file_path_id_front = 'media/' + id_front_name


        id_back = validated_data.pop('id_back')
        id_back_name = self.generate_filename(id_back.name)
        file_path_id_back = 'media/' + id_back_name
        
        selfie = validated_data.pop('selfie')
        selfie_name = self.generate_filename(selfie.name)
        file_path_selfie = 'media/' + selfie_name

        with open(file_path_id_front, 'wb') as destination:
            for chunk in id_front.chunks():
                destination.write(chunk)

        with open(file_path_id_back, 'wb') as destination:
            for chunk in id_back.chunks():
                destination.write(chunk)

        with open(file_path_selfie, 'wb') as destination:
            for chunk in selfie.chunks():
                destination.write(chunk)

        # path_id_front = os.path.join(id)
        return file_path_id_front, file_path_id_back, file_path_selfie

    def generate_filename(self, original_filename):
        # Generate a unique filename for the picture
        unique_name = uuid.uuid4().hex
        ext = os.path.splitext(original_filename)[1]
        return f"{unique_name}{ext}" 