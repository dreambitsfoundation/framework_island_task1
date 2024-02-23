import json
from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth.models import User

TEST_CONTENT_DIRECTORY = "api/tests/test_elements"


class TestUserAndLoginView(TestCase):
    """This is the test suite for User and Login View"""

    def setUp(self) -> None:
        payload = open(f"{TEST_CONTENT_DIRECTORY}/user.json")
        self.payload = json.load(payload)
    
    def test_create_user_account(self):
        client = APIClient()
        response = client.post('/auth/user/', self.payload[0], format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_login(self):
        client = APIClient()
        
        # Create a user instance
        user_payload = self.payload[0]
        user = User(**user_payload)
        user.set_password(user_payload.get("password"))
        user.save()

        # email field is not required in the payload for login.
        user_payload.pop("email")
        
        # Send API request
        response = client.post('/auth/token/', user_payload, format='json')
        self.assertEqual(response.status_code, 200)
