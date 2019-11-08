from django.conf.urls import url

from car_partner.views.car_view import CarViewSet, CarPartnerViewSet
from car_partner.views.partner_view import PartnerViewSet


urlpatterns = [
    url(r'^partners/(?P<pk>[0-9]+)$', PartnerViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    url(r'^partners/$', PartnerViewSet.as_view({'post': 'create'})),

    url(r'^cars/(?P<pk>[0-9]+)$', CarViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    url(r'^cars/$', CarViewSet.as_view({'post': 'create'})),
    url(r'^cars/car_partner/(?P<car_id>[0-9]+)$', CarPartnerViewSet.as_view({'post': 'create'})),
]
