from django.urls import reverse
from rest_framework import status
from rest_framework.test import APILiveServerTestCase

from member.models import User


class MemberTest(APILiveServerTestCase):
    test_username = 'test_username'
    test_password = 'test_password'
    test_first_name = 'test_first_name'
    test_last_name = 'test_last_name'

    def signup_and_return_response(self, extra_data=None):
        url = reverse('rest_signup')
        data = {
            'username': self.test_username,
            'password1': self.test_password,
            'password2': self.test_password,
        }
        if extra_data and isinstance(extra_data, dict):
            data.update(extra_data)
        response = self.client.post(url, data)
        return response

    def test_signup_without_name(self):
        response = self.signup_and_return_response()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('key', response.data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, self.test_username)

    def test_signup(self):
        response = self.signup_and_return_response(
            {'first_name': self.test_first_name, 'last_name': self.test_last_name})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('key', response.data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, self.test_username)

    def test_login(self):
        self.signup_and_return_response()
        url = reverse('rest_login')
        data = {
            'username': self.test_username,
            'password': self.test_password
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.data)

    def test_user_detail(self):
        response = self.signup_and_return_response(
            {'first_name': self.test_first_name, 'last_name': self.test_last_name})
        token = response.data['key']
        url = reverse('rest_profile')
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('pk', response.data)
        self.assertIn('username', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)

        self.assertEqual(self.test_username, response.data.get('username'))
        self.assertEqual(self.test_first_name, response.data.get('first_name'))
        self.assertEqual(self.test_last_name, response.data.get('last_name'))
        self.assertEqual('', response.data.get('email'))
