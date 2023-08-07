import jwt
from walletize.settings import SECRET_KEY

def token_authentication(value):
    user_id = None
    try:
        decoded_token = jwt.decode(value, SECRET_KEY, algorithms=['HS256'])
        if decoded_token['token_type'] == "refresh":
            message = {"message": "You have provided Refresh Token"}
            status = 401
            return(user_id,message, status)
            
        user_id = decoded_token['user_id']
        message = {"message": "Your Token is accepted"}
        status = 200

        return(user_id,message, status)
         
    except jwt.ExpiredSignatureError:
        message = {"message": "Expired Token"}
        status=401
        return(user_id,message, status)

    except jwt.InvalidTokenError:
        message = {"message": "Invalid Token"}
        status=401
        return(user_id,message, status)
    