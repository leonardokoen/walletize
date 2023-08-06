from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignUpSerializer


#Get data. Check if data are valid.
#True : Save User to the database respond with a succesful JSON message
# False: Respond with an error message
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            message = {'message': 'User registered successfully.'}
            return Response(message, status=201)
        return Response(serializer.errors, status=400)