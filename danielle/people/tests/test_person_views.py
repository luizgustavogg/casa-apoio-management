from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from people.models import Person
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

    def test_create_person_just_with_name(self):
        url = '/api/v1/people/'
        data = {'name': 'John Doe'}

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.get(pk=1).name, 'JOHN DOE')

    def test_create_person_with_name_and_cpf(self):
        url = '/api/v1/people/'
        data = {'name': 'John Doe', 'cpf': '51286412013'}

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.client.post(url, data, format='json')
        self.assertEqual(Person.objects.get(pk=1).cpf, '51286412013')

    def test_list_people(self):
        url = '/api/v1/people/'
        data1 = {
            'name': 'John Doe',
            'cpf': '51286412013',
            'city': 'ARACATUBA',
            'postal_code': '00000000'
        }
        data2 = {
            'name': 'Jane Doe',
            'mother_name': 'Fulana Doe',
            'cpf': '12004316004',
            'city': 'ARACATUBA',
            'postal_code': '00000000'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.post(url, data1, format='json')
        self.client.post(url, data2, format='json')
        response = self.client.get(url, format='json')
        self.assertEqual(Person.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], "JOHN DOE")
        self.assertEqual(response.data['results'][0]['cpf'], "51286412013")
        self.assertEqual(response.data['results'][0]['formatted_cpf'],
                         "512.864.120-13")
        self.assertEqual(response.data['results'][0]['postal_code'],
                         "00000000")
        self.assertEqual(response.data['results'][0]['formatted_postal_code'],
                         "00000-000")
        self.assertEqual(response.data['results'][0]['city'], "ARACATUBA")
        self.assertEqual(response.data['results'][1]['name'], "JANE DOE")
        self.assertEqual(response.data['results'][1]['mother_name'],
                         "FULANA DOE")

    def test_list_people_with_12_in_page(self):
        url = '/api/v1/people/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        for _ in range(20):
            fake = Faker()
            data = {"name": fake.name()}
            self.client.post(url, data, format='json')
        response = self.client.get(url, format='json')

        self.assertEqual(response.data['count'], 20)
        self.assertEqual(len(response.data['results']), 12)
