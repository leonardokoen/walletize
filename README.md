# Walletize

This API is organized around REST. It has predictable resource-oriented URLs, accepts form-data and JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes.

## Endpoints

- Sign Up  
- Sign In  
- Refresh Token  
- Account Activation

## Tools

- Django
- PostgreSQL  
- Redis
- Celery
- Docker

## Installation Guide

Clone Repository

```bash
git clone https://github.com/leonardokoen/walletize.git
```

Build Project

```bash
docker-compose up --build
```

## Documentation

### Sign Up Endpoint

Make a POST Request on http://localhost:8000/api/signup/ input format JSON:  

```JSON
{
    "email" :"Email Address",
    "first_name" : "First Name",
    "last_name" : "Last Name",
    "vat_number" : "Vat Number",
    "phone_number" : "Phone Number",
    "password" : "Password",
    "date_of_birth" : "yyyy-mm-dd"
}
```

Example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "email": "drramore@friends.com",
  "first_name": "Joseph",
  "last_name": "Tribiani",
  "vat_number": "1234567890",
  "phone_number": "4566666323",
  "password": "howyoudoin123",
  "date_of_birth": "1990-01-01"
}' http://localhost:8000/api/signup/
```

All fields are Required.

Response in JSON if your registration was successful:

```JSON
{
    "message" : "User registered successfully."
}
```

### Sign In Endpoint

After successful registration make a HTTP POST Request on http://localhost:8000/api/signin/ input format JSON:

```JSON
{
"email" : "Email Address",
"password" : "Password"
}
```

All fields are Required.

Example:

```BASH
curl -X POST -H "Content-Type: application/json" -d '{
  "email": "drramore@friends.com",
  "password": "howyoudoin123"
}' http://localhost:8000/api/signin/
```

Response in JSON if your Sign In was successful:

```JSON
{
    "message" : "You Signed In Successfully",
    "access" : "JSON Web Token",
    "refresh" : "JSON Web Token"
}
```

**access** : a JSON Web Token(JWT) that you will use to activate your account it lasts for 300s.  
**refresh**: a  JSON Web Token(JWT) that you will use to refresh your access token it lasts for 1d.

### Refresh Token Endpoint

If your access JWT expires make a HTTP POST Request on http://localhost:8000/api/token_refresh/ input format JSON:

```JSON
{
    "refresh" : "Your Refresh Token"
}
```

Example

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MTY4ODg4NSwiaWF0IjoxNjkxNjAyNDg1LCJqdGkiOiI5YmNjYzhjZDIxZjg0OGExYjhhZDdmZjI2ODE2MGYyNSIsInVzZXJfaWQiOjV9.KK2FPXl-WMLlfPrtgzLsd1l7I6wOSTYpGIe7ZDp4GV8"
}' http://localhost:8000/api/token_refresh/
```

Response in JSON if your refresh token was valid:

```JSON
{
    "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxNjA0MzcwLCJpYXQiOjE2OTE2MDI0ODUsImp0aSI6ImU5YWM3MTAyODY4ZTQ3NDc4Zjk1NTFjODhiNWFmZjQ4IiwidXNlcl9pZCI6NX0.HN_p1_f3y8DuKN0zm8SZ1S6j-OunGPXVXbUy1f-lv80"
}
```

### Account Activation Endpoint

If you have signed up and signed in successfully and received an access JWT you can make a HTTP POST Request on <http://localhost:8000/api/activation/> using FORM-DATA:

```JSON
{
    "token" : "Your access JWT"
    "id_front" : id_front.jpg
    "id_back" : id_back.jpg
    "selfie" : selfie.jpg
}
```

You should provide your access token and 3 photos, the frond of your ID, the back of your ID and a selfie. 

```bash
curl -X POST -H "Content-Type: multipart/form-data" -F "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxNjA0MzcwLCJpYXQiOjE2OTE2MDI0ODUsImp0aSI6ImU5YWM3MTAyODY4ZTQ3NDc4Zjk1NTFjODhiNWFmZjQ4IiwidXNlcl9pZCI6NX0.HN_p1_f3y8DuKN0zm8SZ1S6j-OunGPXVXbUy1f-lv80" \
-F "id_front=@/path/to/id_front.jpg" \
-F "id_back=@/path/to/id_back.jpg" \
-F "selfie=@/path/to/selfie.jpg" \
http://localhost:8000/api/activate/

```

If the access JWT is valid and you provided 3 photos you will get this Response:

```JSON
{
    "message":"You will receive an email about your account activation result",
    "taskid":"2785d796-d36d-45ee-9be2-7813da01287d"
}
```

**taskid**: Is the id of the background process trying to execute the verification code.

Photos are stored temporary in src/media file. The background process deletes them at the end of its execution.

## Testing

After building and running the containers you can execute the command in another terminal:

```bash
docker container list
```

copy the CONTAINER ID of walletize-django IMAGE

```bash
docker exec -it <CONTAINER ID> bash
```

When you reach the shell of the container execute

```bash
python manage.py test
```

And it will run some prepared tests.

You can access src/api/tests.py and uncomment the test that checks the whole process and background processes.  

Use the command:

```bash
python manage.py test api.tests.BackgroundProcessTestCase.test_succesful_token_verification_and_uploading_pictures
```

## Errors

Everything worked fine before dockerization, after dockerization when trying to send email celery-worker produces the following Error:

```error
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1002)
```

That I could not find a way to resolve. It does not terminate the worker because I have used fail_silently = True. See src/activation/background_task.py
