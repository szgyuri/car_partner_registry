from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from car_partner.constants import OBJECT_IS_DELETED, ERROR
from car_partner.serializers import CarSerializer, CarPartnerSerializer
from car_partner.models import Car, Partner
from car_partner.utils import get_object_from_db, is_object_deleted, str_to_bool


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated,)

    wrapped = openapi.Parameter('wrapped',
                                in_=openapi.IN_QUERY,
                                description='If true, return Partners object, if false return Partner ids',
                                type=openapi.TYPE_BOOLEAN)

    @swagger_auto_schema(manual_parameters=[wrapped])
    def retrieve(self, request, *args, **kwargs):
        wrapped = request.GET.get('wrapped', True)
        if type(wrapped) == str:
            wrapped = str_to_bool(wrapped)
        car_id = kwargs['pk']

        car = get_object_from_db(Car, car_id)
        serializer = CarSerializer(car, context={'wrapped': wrapped})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = CarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        car_id = kwargs['pk']
        car = get_object_from_db(Car, car_id)

        if is_object_deleted(car):
            return Response({ERROR: OBJECT_IS_DELETED}, status=status.HTTP_400_BAD_REQUEST)

        car.deleted_at = datetime.now()
        car.save()
        return Response(status=status.HTTP_200_OK)


class CarPartnerViewSet(viewsets.ModelViewSet):
    serializer_class = CarPartnerSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        car_id = kwargs['car_id']
        car = get_object_from_db(Car, car_id)
        car.partners = []

        serializer = CarPartnerSerializer(request.data)
        for partner_id in serializer.data['partner_ids']:
            partner = get_object_from_db(Partner, partner_id)
            car.partners.add(partner)

        car.save()
        return Response(CarSerializer(car).data, status=status.HTTP_201_CREATED)
