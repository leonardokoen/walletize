from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from .models import User


# class UserRegistrationTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_user_registration(self):
#         data = {
#             'first_name': 'le',
#             'last_name': 'Doe',
#             'vat_number': '123456789',
#             'date_of_birth': '1990-01-01',
#             'phone_number': '1234567890',
#             'email': 'john.doe@example.com',
#             'password': 'password123' ,  
#         }
#         response = self.client.post('http://127.0.0.1:8000/register/', data, format='json')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.data['message'], 'User registered successfully.')
#         print("Successful database entry!")


class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    

    def test_user_authentication(self):

        data_enter_database = {
            'first_name': 'le',
            'last_name': 'Doe',
            'vat_number': '123456789',
            'date_of_birth': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'password123' ,  
        }
        response = self.client.post('http://127.0.0.1:8000/signup/', data_enter_database, format='json')

        data_signin = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }

        response = self.client.post('http://127.0.0.1:8000/signin/', data_signin, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)


# Create your tests here.





