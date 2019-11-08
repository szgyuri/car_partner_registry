from rest_framework import status
from rest_framework.test import force_authenticate

from car_partner.constants import DELETED_AT_NULL_VALUE, ERROR, OBJECT_IS_DELETED
from car_partner.models import Car, Partner
from car_partner.tests.tests import ViewSetParentTestCase
from car_partner.views.car_view import CarViewSet


class CreateCarViewTestCase(ViewSetParentTestCase):

    @classmethod
    def setUpClass(cls):
        super(CreateCarViewTestCase, cls).setUpClass()
        cls.method_dict = {'post': 'create'}

    def setUp(self):
        self.valid_payload = {
            "average_fuel": 5.4,
            "delegation_starting": 123,
            "delegation_ending": 456,
            "driver": "test_driver",
            "owner": "test_owner",
            "type": "céges",
            "deleted_at": 0
        }

    def test_with_valid_payload(self):
        request = self.factory.post('/api/cars', self.valid_payload)
        force_authenticate(request, user=self.user, token=self.token.key)
        view = CarViewSet.as_view(self.method_dict)

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_with_invalid_payload(self):
        self.valid_payload["average_fuel"] = "asd"
        invalid_payload = self.valid_payload
        request = self.factory.post('/api/cars', invalid_payload)
        force_authenticate(request, user=self.user, token=self.token.key)
        view = CarViewSet.as_view(self.method_dict)

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetCarViewTestCase(ViewSetParentTestCase):

    @classmethod
    def setUpClass(cls):
        super(GetCarViewTestCase, cls).setUpClass()
        cls.method_dict = {'get': 'retrieve'}

    def setUp(self):
        self.car = Car(average_fuel=5.4, delegation_starting=123, delegation_ending=456, driver="test_driver",
                       owner="test_owner", type="céges", deleted_at=None)
        self.car.save()
        self.partner = Partner(name="test_partner", city='Bp', address='Random Str', company_name='RoadRecord',
                               created_at=234, modified_at=567, deleted_at=None)
        self.partner.save()

    def test_with_valid_id(self):
        request = self.factory.get('/api/cars/' + str(self.car.id))
        force_authenticate(request, user=self.user, token=self.token.key)
        view = CarViewSet.as_view(self.method_dict)

        response = view(request, pk=self.car.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.car.id)

    def test_with_invalid_id(self):
        invalid_id = 999
        request = self.factory.get('/api/cars/' + str(invalid_id))
        force_authenticate(request, user=self.user, token=self.token.key)
        view = CarViewSet.as_view(self.method_dict)

        response = view(request, pk=invalid_id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrapped_param_true_without_partners(self):
        request = self.factory.get('/api/cars/' + str(self.car.id) + '?wrapped=true')
        force_authenticate(request, user=self.user, token=self.token.key)
        view = CarViewSet.as_view(self.method_dict)

        response = view(request, pk=self.car.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['partners']), len(self.car.partners.all()))

    def test_wrapped_param_true_with_partners(self):
        self.car.partners = []
        self.car.partners.add(self.partner)
        self.car.save()
        request = self.factory.get('/api/cars/' + str(self.car.id) + '?wrapped=true')
        force_authenticate(request, user=self.user, token=self.token.key)
        view = CarViewSet.as_view(self.method_dict)

        response = view(request, pk=self.car.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['partners'][0], self.partner.id)

    def test_wrapped_param_false_with_partners(self):
        self.car.partners = []
        self.car.partners.add(self.partner)
        self.car.save()
        request = self.factory.get('/api/cars/' + str(self.car.id) + '?wrapped=false')
        force_authenticate(request, user=self.user, token=self.token.key)
        view = CarViewSet.as_view(self.method_dict)

        response = view(request, pk=self.car.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['partners'][0]), len(self.partner.__dict__))
        self.assertEqual(response.data['partners'][0]['name'], self.partner.name)


class DeleteCarViewTestCase(ViewSetParentTestCase):

    @classmethod
    def setUpClass(cls):
        super(DeleteCarViewTestCase, cls).setUpClass()
        cls.method_dict = {'delete': 'destroy'}

    def setUp(self):
        self.car = Car(average_fuel=5.4, delegation_starting=123, delegation_ending=456, driver="test_driver",
                       owner="test_owner", type="céges", deleted_at=None)
        self.car.save()

    def test_with_not_deleted_obj(self):
        request = self.factory.delete('/api/cars/' + str(self.car.id))
        force_authenticate(request, user=self.user, token=self.token.key)
        view = CarViewSet.as_view(self.method_dict)

        response = view(request, pk=self.car.id)

        deleted_car = Car.objects.get(pk=self.car.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(deleted_car.deleted_at, DELETED_AT_NULL_VALUE)

    def test_with_already_deleted_obj(self):
        self.car.deleted_at = 34456
        self.car.save()
        request = self.factory.delete('/api/cars/' + str(self.car.id))
        force_authenticate(request, user=self.user, token=self.token.key)
        view = CarViewSet.as_view(self.method_dict)

        response = view(request, pk=self.car.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[ERROR], OBJECT_IS_DELETED)

    def test_with_invalid_id(self):
        invalid_id = 999
        request = self.factory.delete('/api/cars/' + str(invalid_id))
        force_authenticate(request, user=self.user, token=self.token.key)
        view = CarViewSet.as_view(self.method_dict)

        response = view(request, pk=invalid_id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
