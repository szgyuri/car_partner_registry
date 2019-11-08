import unittest

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory


class ViewSetParentTestCase(unittest.TestCase):
    user = None
    username = 'my_test_user'
    email = 'test@test.com'
    password = 'pass'

    @classmethod
    def setUpClass(cls):
        user_query_set = User.objects.filter(username=cls.username)
        if len(user_query_set) == 0:
            cls.user = User.objects.create_user(username=cls.username, email=cls.email, password=cls.password)
            cls.token = Token.objects.create(user=cls.user)
            cls.token.save()
        else:
            cls.user = user_query_set[0]
            cls.token = Token.objects.filter(user=cls.user)[0]

        cls.factory = APIRequestFactory()
