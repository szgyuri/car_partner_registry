from rest_framework import status
from rest_framework.test import force_authenticate

from car_partner.models import Partner, Car
from car_partner.tests.tests import ViewSetParentTestCase
from car_partner.views.car_view import CarPartnerViewSet


class CreateCarPartnerViewTestCase(ViewSetParentTestCase):
    @classmethod
    def setUpClass(cls):
        super(CreateCarPartnerViewTestCase, cls).setUpClass()
        cls.method_dict = {'post': 'create'}

    def setUp(self):
        self.car = Car(average_fuel=5.4, delegation_starting=123, delegation_ending=456, driver="test_driver",
                       owner="test_owner", type="céges", deleted_at=None)
        self.car.save()
        self.partner = Partner(name="test_partner", city='Bp', address='Random Str', company_name='RoadRecord',
                               created_at=234, modified_at=567, deleted_at=None)
        self.partner.save()

        self.valid_payload = {
            "partner_ids": [self.partner.id]
        }

    def test_with_valid_partner_id(self):
        request = self.factory.post('/api/cars' + str(self.car.id), self.valid_payload)
        force_authenticate(request, user=self.user, token=self.token.key)
        view = CarPartnerViewSet.as_view(self.method_dict)

        response = view(request, car_id=self.car.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['partners'][0], self.partner.id)

    def test_with_invalid_partner_id(self):
        self.valid_payload["partner_ids"] = [999]
        invalid_payload = self.valid_payload
        request = self.factory.post('/api/cars' + str(self.car.id), invalid_payload)
        force_authenticate(request, user=self.user, token=self.token.key)
        view = CarPartnerViewSet.as_view(self.method_dict)

        response = view(request, car_id=self.car.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
