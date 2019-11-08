from datetime import datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from car_partner.constants import OBJECT_IS_DELETED, ERROR
from car_partner.serializers import PartnerSerializer
from car_partner.models import Partner
from car_partner.utils import get_object_from_db, is_object_deleted, str_to_bool


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = (IsAuthenticated,)

    wrapped = openapi.Parameter('wrapped',
                                in_=openapi.IN_QUERY,
                                description='If true, return Cars object, if false return Car ids',
                                type=openapi.TYPE_BOOLEAN)

    @swagger_auto_schema(manual_parameters=[wrapped])
    def retrieve(self, request, *args, **kwargs):
        wrapped = request.GET.get('wrapped', True)
        if type(wrapped) == str:
            wrapped = str_to_bool(wrapped)
        partner_id = kwargs['pk']

        partner = get_object_from_db(Partner, partner_id)
        serializer = PartnerSerializer(partner, context={'wrapped': wrapped})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = PartnerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        partner_id = kwargs['pk']
        partner = get_object_from_db(Partner, partner_id)

        if is_object_deleted(partner):
            return Response({ERROR: OBJECT_IS_DELETED}, status=status.HTTP_400_BAD_REQUEST)

        partner.deleted_at = datetime.now()
        partner.save()
        return Response(status=status.HTTP_200_OK)
