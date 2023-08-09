import jwt
from walletize.settings import SECRET_KEY

# Perform custom JWT authentication
def token_authentication(received_token):
    # Set default user_id = None in case of an error
    user_id = None
    try:
        #Decode JWT using SECRET_KEY
        decoded_token = jwt.decode(received_token, SECRET_KEY, algorithms=['HS256'])
        if decoded_token['token_type'] == "refresh":
            message = {"message": "You have provided Refresh Token"}
            status = 401
            return(user_id,message, status)
            
        user_id = decoded_token['user_id']
        message = {"message": "Your Token is accepted"}
        status = 200

        return(user_id,message, status)
    
    # Error Handlers
    except jwt.ExpiredSignatureError:
        message = {"message": "Expired Token"}
        status=401
        return(user_id,message, status)

    except jwt.InvalidTokenError:
        message = {"message": "Invalid Token"}
        status=401
        return(user_id,message, status)


# For test purposes
def expired_token(token):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    decoded_token['exp'] = decoded_token['exp'] - 3600
    expired_token = jwt.encode(decoded_token, SECRET_KEY, algorithm='HS256')
    return(expired_token)
    