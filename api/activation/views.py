from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ActivationSerializer
from .token_authentication import token_authentication
from api.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from .background_task import photo_validation


class UserActivationView(APIView):

    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid():
            # id_front_name, id_back_name, selfie_name = serializer.save()
            
            value = serializer.validated_data['token']
            user_id, message, status = token_authentication(value)
            if user_id == None:
                return Response(message, status)
        
            user = User.objects.get(id = user_id)
            if user.is_active:
                message = {"message": "You have already activated your account"}
                return Response(message, status = 409)
            else:
                file_path_id_front, file_path_id_back, file_path_selfie = serializer.save()
                photo_validation.delay(file_path_id_front, file_path_id_back, file_path_selfie, user_id)
                message = {"message": "Horray"}
                return Response(message, status = 200)
        return Response(serializer.errors, status=400)
    
    

            

        




    
        
        
            