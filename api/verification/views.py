from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TokenSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
import jwt
from walletize.settings import SECRET_KEY
from api.models import User

class TokenAuthenticationView(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            value = serializer.validated_data['token']
            try:
                decoded_token = jwt.decode(value, SECRET_KEY, algorithms=['HS256'])
                if decoded_token['token_type'] == "refresh":
                    return Response({"message": "You have provided Refresh Token"}, status = 401)
                
                user = User.objects.get(id=decoded_token['user_id'])
                if user.is_active:
                    return Response({"message": "You have already activated your account"}, status = 401)
                else:
                    pass
                return Response({"message": "Hi"}, status = 200)
            
            except jwt.ExpiredSignatureError:
                return Response({"message": "Expired Token"}, status=400) 
            except jwt.InvalidTokenError:
                return Response({"message": "Invalid Token"}, status = 401)
        else:
            return Response(serializer.errors, status=400)
        
        
            