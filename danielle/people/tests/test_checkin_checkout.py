from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from people.models import Checkin, Person, checkin
from faker import Faker


class PersonViewTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user('test',
                                        email='testuser@test.com',
                                        password='test')

    def test_create_simple_checkin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        person_url = '/api/v1/people/'
        person_data = {'name': 'John Doe'}
        self.client.post(person_url, person_data, format='json')

        checkin_url = '/api/v1/checkins/'
        checkin_data = {'person': 1, 'reason': 'professional'}
        checkin_response = self.client.post(checkin_url,
                                            checkin_data,
                                            format='json')

        self.assertEqual(checkin_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Checkin.objects.count(), 1)
        self.assertEqual(Checkin.objects.get(pk=1).person_name, 'JOHN DOE')
