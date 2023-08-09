# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from .models import User
from api.activation.token_authentication import token_authentication, expired_token


#python manage.py test

class SigUpTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_correct_user_registration(self):
        print("-test_correct_user_registration")
        data = {
            'first_name': 'le',
            'last_name': 'Doe',
            'vat_number': '123456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'User registered successfully.')

    def test_missing_fields(self):
        print("-test_missing_fields")

        # Missing Fields
        data = {
            'first_name': 'le',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            # 'password': 'password123' ,
            # 'vat_number': '123456789'
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data, format='json')
        self.assertEqual(response.status_code, 400)

        response_data_key_names = list(response.data.keys())

        for keys in response_data_key_names:
            self.assertEqual(response.data[keys], ["This field is required."])
        
    def test_user_already_exists(self):
        print("-test_user_already_exists")
        data = {
            'first_name': 'le',
            'last_name': 'Doe',
            'vat_number': '123456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'User registered successfully.')

        same_email = {
            'first_name': 'JeLo',
            'last_name': 'lELE',
            'vat_number': '12322456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', same_email, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'],  ["User with this email already exists."])

    def test_invalid_email(self):
        print("-test_invalid_email")
        data = {
            'first_name': 'le',
            'last_name': 'Doe',
            'vat_number': '123456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doeexample.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'],  ["Enter a valid email address."])

    def test_missing_fields_and_ivalid_or_existing_email(self):
        print("-test_missing_fields_and_ivalid_or_existing_email")
        #Make a successful entry
        data = {
            'first_name': 'le',
            'last_name': 'Doe',
            'vat_number': '123456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'User registered successfully.')

        # Try register someone with the same email and missing fields
        data = {
            'first_name': 'JeLo',
            'last_name': 'lELE',
            'vat_number': '12322456789',
            'date_of_birth': '1990-01-01',
            # 'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            # 'password': 'password123' ,  
        }

        response = self.client.post('http://127.0.0.1:8000/api/signup/', data, format='json')
        response_data_key_names = list(response.data.keys())
        if ("email" in response_data_key_names):
            if response.data['email'][0] == "Enter a valid email address." :
                response_data_key_names.remove('email')
                self.assertEqual(response.data['email'], ["Enter a valid email address."])
            if response.data['email'][0] == "User with this email already exists.":
                response_data_key_names.remove('email')
                self.assertEqual(response.data['email'], ["User with this email already exists."])

        for keys in response_data_key_names:
            self.assertEqual(response.data[keys], ["This field is required."])

        # Try register someone with invalid email and missing fields
        data = {
            'first_name': 'JeLo',
            'last_name': 'lELE',
            'vat_number': '12322456789',
            'date_of_birth': '1990-01-01',
            # 'phone_number': '1234567890',
            'email': 'john.doeexample.com',
            # 'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data, format='json')
        response_data_key_names = list(response.data.keys())
        if ("email" in response_data_key_names):
            if response.data['email'][0] == "Enter a valid email address." :
                response_data_key_names.remove('email')
                self.assertEqual(response.data['email'], ["Enter a valid email address."])
            if response.data['email'][0] == "User with this email already exists.":
                response_data_key_names.remove('email')
                self.assertEqual(response.data['email'], ["User with this email already exists."])

        for keys in response_data_key_names:
            self.assertEqual(response.data[keys], ["This field is required."])


class SignInTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_sign_in_succesfully(self):
        print("-test_sign_in_succesfully")
        # register someone in database
        data_enter_database = {
            'first_name': 'le',
            'last_name': 'Doe',
            'vat_number': '123456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data_enter_database, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'User registered successfully.')

        data_signin = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }

        response = self.client.post('http://127.0.0.1:8000/api/signin/', data_signin, format='json')
        self.assertEqual(response.status_code, 200)

    def test_wrong_credentials(self):
        print("-test_wrong_credentials")
        data_database = {
            'first_name': 'le',
            'last_name': 'Doe',
            'vat_number': '123456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data_database, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'User registered successfully.')

        data_signin = {
            'email': 'john.doe@example.com',
            'password': 'password' #missing123
        }

        response = self.client.post('http://127.0.0.1:8000/api/signin/', data_signin, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'], ['Invalid email or password.'])

        data_signin = {
            'email': 'john.doe@exampl.com', #misspelled email
            'password': 'password123' 
        }

        response = self.client.post('http://127.0.0.1:8000/api/signin/', data_signin, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'], ['Invalid email or password.'])

class RefreshTokenTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_send_acceptable_refresh_token(self):
        print("-test_send_acceptable_refresh_token")
        data_database = {
            'first_name': 'le',
            'last_name': 'Doe',
            'vat_number': '123456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data_database, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'User registered successfully.')

        data_signin = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }

        response = self.client.post('http://127.0.0.1:8000/api/signin/', data_signin, format='json')
        self.assertEqual(response.status_code, 200)

        refresh_token = response.data['refresh']

        refresh = {
            "refresh" : refresh_token
        }

        response = self.client.post('http://127.0.0.1:8000/api/token_refresh/', refresh, format='json')
        self.assertEqual(response.status_code, 200)

    def test_send_non_acceptable_refresh_token(self):

        print("-test_send_non_acceptable_refresh_token")
        refresh = {
            "refresh" : 122212
        }

        response = self.client.post('http://127.0.0.1:8000/api/token_refresh/', refresh, format='json')
        self.assertTrue(response.status_code == 400 or response.status_code == 401)

class ActivationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_invalid_token(self):
        print("-test_invalid_token")
        form_data = {
            'token': "fgrer2344fgg34rttght34tgrg34t3g5t34t44t34t",
            'id_front': ('lena1.png', open('./api/test_images/lenna.png', 'rb')),
            'id_back': ('lena2.png', open('./api/test_images/lenna.png', 'rb')),
            'selfie': ('lena3.png', open('./api/test_images/lenna.png', 'rb'))
        }
        response = self.client.post('http://127.0.0.1:8000/api/activate/', data = form_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], "Invalid Token")

    def test_expired_token(self):

        print("-test_expired_token")
        data = {
            'first_name': 'le',
            'last_name': 'Doe',
            'vat_number': '123456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'User registered successfully.')

        data_signin = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }

        response = self.client.post('http://127.0.0.1:8000/api/signin/', data_signin, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.data['access']
        token = expired_token(token)
        form_data = {
            'token': token,
            'id_front': ('lena1.png', open('./api/test_images/lenna.png', 'rb')),
            'id_back': ('lena2.png', open('./api/test_images/lenna.png', 'rb')),
            'selfie': ('lena3.png', open('./api/test_images/lenna.png', 'rb'))
        }
        response = self.client.post('http://127.0.0.1:8000/api/activate/', data = form_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], "Expired Token")

    def test_provided_refresh_instead_of_access(self):
        print("-test_provided_refresh_instead_of_access")
        data = {
            'first_name': 'le',
            'last_name': 'Doe',
            'vat_number': '123456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'User registered successfully.')

        data_signin = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }

        response = self.client.post('http://127.0.0.1:8000/api/signin/', data_signin, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.data['refresh']

        form_data = {
            'token': token,
            'id_front': ('lena1.png', open('./api/test_images/lenna.png', 'rb')),
            'id_back': ('lena2.png', open('./api/test_images/lenna.png', 'rb')),
            'selfie': ('lena3.png', open('./api/test_images/lenna.png', 'rb'))
        }
        response = self.client.post('http://127.0.0.1:8000/api/activate/', data = form_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], "You have provided Refresh Token")

    def test_invalid_file_or_missing_an_image_field(self):
        print("-test_invalid_file_or_missing_an_image_field")
        data = {
            'first_name': 'le',
            'last_name': 'Doe',
            'vat_number': '123456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'User registered successfully.')

        data_signin = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }

        response = self.client.post('http://127.0.0.1:8000/api/signin/', data_signin, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.data['refresh']

        form_data = {
            'token': token,
            'id_front': ('lena1.png', open('./api/test_images/lenna.png', 'rb')),
            'id_back': ('lena2.png', open('./api/test_images/lenna.png', 'rb')),
            # 'selfie': ('lena3.png', open('./api/test_images/lenna.png', 'rb'))
        }
        response = self.client.post('http://127.0.0.1:8000/api/activate/', data = form_data)

        self.assertEqual(response.status_code, 400)

        
    def test_user_is_already_activated(self):
        print("-test_user_already_activated")
        data = {
            'first_name': 'le',
            'last_name': 'Doe',
            'vat_number': '123456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/api/signup/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'User registered successfully.')

        data_signin = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }

        response = self.client.post('http://127.0.0.1:8000/api/signin/', data_signin, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.data['access']
        id,_,_ = token_authentication(token)
        user = User.objects.get(id = id)
        user.is_active = True
        user.save()

        form_data = {
            'token': token,
            'id_front': ('lena1.png', open('./api/test_images/lenna.png', 'rb')),
            'id_back': ('lena2.png', open('./api/test_images/lenna.png', 'rb')),
            'selfie': ('lena3.png', open('./api/test_images/lenna.png', 'rb'))
        }
        response = self.client.post('http://127.0.0.1:8000/api/activate/', data = form_data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['message'], "You have already activated your account")

#If you want to run the whole procedure successfully uncomment the following code
#python manage.py test api.tests.BackgroundProcessTestCase.test_succesful_token_verification_and_uploading_pictures
#Run this piece of code alone because the background process interferes with the other tests and raises an error.

# class BackgroundProcessTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#     def test_succesful_token_verification_and_uploading_pictures(self):
#         print("-test_succesful_token_verification_and_uploading_pictures")
#         data = {
#             'first_name': 'le',
#             'last_name': 'Doe',
#             'vat_number': '123456789',
#             'date_of_birth': '1990-01-01',
#             'phone_number': '1234567890',
#             'email': 'john.doe@example.com',
#             'password': 'password123' ,  
#         }
#         response = self.client.post('http://127.0.0.1:8000/api/signup/', data, format='json')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.data['message'], 'User registered successfully.')

#         data_signin = {
#             'email': 'john.doe@example.com',
#             'password': 'password123'
#         }

#         response = self.client.post('http://127.0.0.1:8000/api/signin/', data_signin, format='json')
#         self.assertEqual(response.status_code, 200)
#         token = response.data['access']
        
#         form_data = {
#             'token': token,
#             'id_front': ('lena1.png', open('./api/test_images/lenna.png', 'rb')),
#             'id_back': ('lena2.png', open('./api/test_images/lenna.png', 'rb')),
#             'selfie': ('lena3.png', open('./api/test_images/lenna.png', 'rb'))
#         }
#         response = self.client.post('http://127.0.0.1:8000/api/activate/', data = form_data)
#         taskid = response.data['taskid']

#         if response.status_code == 200:
#             print("--------------------------------------------------")
#             print("Activation Background Process:")
#             print("-Your Data are currently processing in the background.")
#             print("-When the files from media folder are deleted, indicates that the background process has finished")
#             print("--------------------------------------------------")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['message'], "You will receive an email about your account activation result")






