from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ActivationSerializer
from .token_authentication import token_authentication
from api.models import User
from rest_framework.parsers import MultiPartParser, FormParser

class UserActivationView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid():
            value = serializer.validated_data['token']
            user_id, message, status = token_authentication(value)
            if user_id == None:
                return Response(message, status)
            user = User.objects.get(id = user_id)
            id_front = serializer.validated_data['id_front']
            id_back = serializer.validated_data['id_back']
            selfie = serializer.validated_data['selfie']
            if user.is_active:
                message = {"message": "You have already activated your account"}
                return Response(message, status = 409)
            else:
                
                message = {"message": "Horray"}
                return Response(message, status = 200)
        return Response(serializer.errors, status=400)
            

        




    
        
        
            