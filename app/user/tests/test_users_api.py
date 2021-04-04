from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""

        payload = {
            'email': 'test@company.com',
            'password': 'testpass1',
            'name': 'Test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user already exists fails"""

        payload = {
            'email': 'test@company.com',
            'password': 'testpass1',
            'name': 'Test name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 8 character"""

        payload = {
            'email': 'test@company.com',
            'password': 'pass123',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that the token is created"""

        payload = {
            'email': 'test@company.com',
            'password': 'testpass1',
            'name': 'Test name'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        """Test that the token is not created if credentials are not valid"""

        create_user(email='test@company.com', password='testpass1')
        payload = {
            'email': 'test@company.com',
            'password': 'thisIsTotalyWrong',
            'name': 'Test name'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if the user doesn't exist"""

        payload = {
            'email': 'test@company.com',
            'password': 'testpass1',
            'name': 'Test name'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertIn('non_field_errors', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_pasword_field(self):
        """Test that token is not created if password field is missing"""

        res = self.client.post(TOKEN_URL, {
            'email': 'test@company.com', 'password': ''}
            )

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', res.data)

    def test_create_token_missing_email_field(self):
        """Test that the token is not created if the email field is missing"""

        res = self.client.post(TOKEN_URL, {
            'email': '', 'password': 'passtest1'}
            )

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data)
