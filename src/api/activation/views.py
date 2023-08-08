from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ActivationSerializer
from .token_authentication import token_authentication
from api.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from .background_task import photo_validation

# Main Activation Procedure
class UserActivationView(APIView):
    #Parsers for the incoming data(token , 3 photo files)
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        #Call the serializer
        serializer = ActivationSerializer(data=request.data)
        #Check if serialization was valid else Respond with Error
        if serializer.is_valid():
            
            #Take the validated token
            value = serializer.validated_data['token']

            #Use custom authentication return users_id in database, message and status 
            user_id, message, status = token_authentication(value)

            #Check if user_id is None that means authentication Raised an Error 
            if user_id == None:
                return Response(message, status)

            # Check if user is already active
            # Else:
            # Save files in the media folder
            # Add photo validation to background queue by providing paths to files and user_id
            # Response status = 200
            user = User.objects.get(id = user_id)
            if user.is_active:
                message = {"message": "You have already activated your account"}
                return Response(message, status = 409)
            else:
                file_path_id_front, file_path_id_back, file_path_selfie = serializer.save()
                photo_validation.delay(file_path_id_front, file_path_id_back, file_path_selfie, user_id)
                message = {"message": "You will receive an email about your account activation result"}
                return Response(message, status = 200)
        return Response(serializer.errors, status=400)
    
    

            

        




    
        
        
            