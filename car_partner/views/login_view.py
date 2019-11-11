from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from car_partner.constants import ERROR, INVALID_CREDENTIALS, USERNAME_OR_PASS_NOT_FILLED


class LoginViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        if username is None or password is None:
            return Response({ERROR: USERNAME_OR_PASS_NOT_FILLED}, status=HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({ERROR: INVALID_CREDENTIALS}, status=HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=HTTP_200_OK)
