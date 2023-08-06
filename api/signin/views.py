from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignInSerializer
from rest_framework.exceptions import AuthenticationFailed


#If authentication was succesful it won't raise an error
#and it will return a message and a token to the user

#If an error is raised the error handler will deal with 
#the error respond with the JSON message 'Invalid email or password.'
class SignInView(APIView):

    def post(self, request):

        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        token_refresh = str(refresh)
        token_access = str(refresh.access_token)
        return Response({'message': 'You Signed In Successfully','access_token (300s)': token_access, 'refresh_token (1 day)': token_refresh}, status=200)
    
    def handle_exception(self, exc):
        if isinstance(exc, AuthenticationFailed):
            return Response({'error': 'Invalid email or password.'}, status=401)
        return super().handle_exception(exc) 