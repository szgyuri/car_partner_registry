from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.views import APIView

from car_partner.constants import ERROR, INVALID_CREDENTIALS, USERNAME_OR_PASS_NOT_FILLED


class LoginView(APIView):
    permission_classes = (AllowAny,)

    username = openapi.Parameter('username', in_=openapi.IN_QUERY,
                                 description='Username for login', type=openapi.TYPE_STRING)
    password = openapi.Parameter('password', in_=openapi.IN_QUERY,
                                 description='Password for login', type=openapi.TYPE_STRING)

    @staticmethod
    @swagger_auto_schema(manual_parameters=[username, password])
    def post(request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if username is None or password is None:
            return Response({ERROR: USERNAME_OR_PASS_NOT_FILLED}, status=HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({ERROR: INVALID_CREDENTIALS}, status=HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=HTTP_200_OK)
