from rest_framework import status
from rest_framework.test import force_authenticate

from car_partner.constants import DELETED_AT_NULL_VALUE, ERROR, OBJECT_IS_DELETED
from car_partner.models import Car, Partner
from car_partner.tests.tests import ViewSetParentTestCase
from car_partner.views.partner_view import PartnerViewSet


class CreatePartnerViewTestCase(ViewSetParentTestCase):

    @classmethod
    def setUpClass(cls):
        super(CreatePartnerViewTestCase, cls).setUpClass()
        cls.method_dict = {'post': 'create'}

    def setUp(self):
        self.valid_payload = {
            "name": "test_name",
            "city": "Bp",
            "address": "R Str.",
            "company_name": "RoadRecord",
            "deleted_at": 0
        }

    def test_with_valid_payload(self):
        request = self.factory.post('/api/partners', self.valid_payload)
        force_authenticate(request, user=self.user, token=self.token.key)
        view = PartnerViewSet.as_view(self.method_dict)

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_with_invalid_payload(self):
        self.valid_payload["deleted_at"] = "asd"
        invalid_payload = self.valid_payload
        request = self.factory.post('/api/partners', invalid_payload)
        force_authenticate(request, user=self.user, token=self.token.key)
        view = PartnerViewSet.as_view(self.method_dict)

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetPartnerViewTestCase(ViewSetParentTestCase):

    @classmethod
    def setUpClass(cls):
        super(GetPartnerViewTestCase, cls).setUpClass()
        cls.method_dict = {'get': 'retrieve'}

    def setUp(self):
        self.partner = Partner(name="test_partner", city='Bp', address='Random Str', company_name='RoadRecord',
                               created_at=234, modified_at=567, deleted_at=None)
        self.partner.save()
        self.car = Car(average_fuel=5.4, delegation_starting=123, delegation_ending=456, driver="test_driver",
                       owner="test_owner", type="céges", deleted_at=None)
        self.car.save()

    def test_with_valid_id(self):
        request = self.factory.get('/api/partners/' + str(self.partner.id))
        force_authenticate(request, user=self.user, token=self.token.key)
        view = PartnerViewSet.as_view(self.method_dict)

        response = view(request, pk=self.partner.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.partner.id)

    def test_with_invalid_id(self):
        invalid_id = 999
        request = self.factory.get('/api/partners/' + str(invalid_id))
        force_authenticate(request, user=self.user, token=self.token.key)
        view = PartnerViewSet.as_view(self.method_dict)

        response = view(request, pk=invalid_id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrapped_param_true_without_cars(self):
        cars_count = 0
        request = self.factory.get('/api/partners/' + str(self.partner.id) + '?wrapped=true')
        force_authenticate(request, user=self.user, token=self.token.key)
        view = PartnerViewSet.as_view(self.method_dict)

        response = view(request, pk=self.partner.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['cars']), cars_count)

    def test_wrapped_param_true_with_cars(self):
        self.car.partners = []
        self.car.partners.add(self.partner)
        self.car.save()
        request = self.factory.get('/api/partners/' + str(self.partner.id) + '?wrapped=true')
        force_authenticate(request, user=self.user, token=self.token.key)
        view = PartnerViewSet.as_view(self.method_dict)

        response = view(request, pk=self.partner.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cars'][0], self.car.id)

    def test_wrapped_param_false_with_cars(self):
        self.car.partners = []
        self.car.partners.add(self.partner)
        self.car.save()
        request = self.factory.get('/api/partners/' + str(self.partner.id) + '?wrapped=false')
        force_authenticate(request, user=self.user, token=self.token.key)
        view = PartnerViewSet.as_view(self.method_dict)

        response = view(request, pk=self.partner.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['cars'][0]), len(self.car.__dict__))
        self.assertEqual(response.data['cars'][0]['driver'], self.car.driver)


class DeletePartnerViewTestCase(ViewSetParentTestCase):

    @classmethod
    def setUpClass(cls):
        super(DeletePartnerViewTestCase, cls).setUpClass()
        cls.method_dict = {'delete': 'destroy'}

    def setUp(self):
        self.partner = Partner(name="test_partner", city='Bp', address='Random Str', company_name='RoadRecord',
                               created_at=234, modified_at=567, deleted_at=None)
        self.partner.save()

    def test_with_not_deleted_obj(self):
        request = self.factory.delete('/api/partners/' + str(self.partner.id))
        force_authenticate(request, user=self.user, token=self.token.key)
        view = PartnerViewSet.as_view(self.method_dict)

        response = view(request, pk=self.partner.id)

        deleted_partner = Partner.objects.get(pk=self.partner.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(deleted_partner.deleted_at, DELETED_AT_NULL_VALUE)

    def test_with_already_deleted_obj(self):
        self.partner.deleted_at = 34456
        self.partner.save()
        request = self.factory.delete('/api/partners/' + str(self.partner.id))
        force_authenticate(request, user=self.user, token=self.token.key)
        view = PartnerViewSet.as_view(self.method_dict)

        response = view(request, pk=self.partner.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[ERROR], OBJECT_IS_DELETED)

    def test_with_invalid_id(self):
        invalid_id = 999
        request = self.factory.delete('/api/partners/' + str(invalid_id))
        force_authenticate(request, user=self.user, token=self.token.key)
        view = PartnerViewSet.as_view(self.method_dict)

        response = view(request, pk=invalid_id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
