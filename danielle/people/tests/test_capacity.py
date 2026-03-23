from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from people.models import Checkin, Person, HouseConfiguration, Checkout


class HouseCapacityTests(APITestCase):
    """
    Testes para validar a funcionalidade de controle de capacidade
    e disponibilidade de vagas da casa de apoio.
    """
    
    def setUp(self):
        """Configuração inicial para cada teste."""
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        
        # Configurar a capacidade máxima para 2 vagas
        self.config = HouseConfiguration.get_config()
        self.config.max_capacity = 2
        self.config.save()
        
        # Criar algumas pessoas para os testes
        self.person1 = Person.objects.create(name='Pessoa 1')
        self.person2 = Person.objects.create(name='Pessoa 2')
        self.person3 = Person.objects.create(name='Pessoa 3')
    
    @staticmethod
    def setup_user():
        """Cria um usuário para autenticação."""
        User = get_user_model()
        return User.objects.create_user(
            'test_capacity',
            email='test_capacity@test.com',
            password='test123'
        )
    
    def test_checkin_with_available_vacancy(self):
        """
        Teste 1: Criar check-in quando há vagas disponíveis.
        Esperado: Sucesso (status 201).
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        checkin_url = '/api/v1/checkins/'
        checkin_data = {
            'person': self.person1.id,
            'reason': 'professional'
        }
        
        response = self.client.post(checkin_url, checkin_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Checkin.objects.count(), 1)
        self.assertEqual(Checkin.objects.get(pk=1).person_name, 'Pessoa 1')
    
    def test_checkin_at_full_capacity(self):
        """
        Teste 2: Tentar criar check-in quando a casa está em capacidade máxima.
        Esperado: Erro (status 400) com mensagem clara sobre falta de vagas.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Preencher as 2 vagas disponíveis
        Checkin.objects.create(
            person=self.person1,
            reason='professional',
            active=True
        )
        Checkin.objects.create(
            person=self.person2,
            reason='professional',
            active=True
        )
        
        # Tentar criar um terceiro check-in (sem vagas)
        checkin_url = '/api/v1/checkins/'
        checkin_data = {
            'person': self.person3.id,
            'reason': 'professional'
        }
        
        response = self.client.post(checkin_url, checkin_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Checkin.objects.count(), 2)
        self.assertIn('Casa de apoio em capacidade máxima', str(response.data))
    
    def test_vacancy_available_after_checkout(self):
        """
        Teste 3: Verificar se vaga é liberada após check-out.
        Esperado: Após checkout, a vaga deve ficar disponível.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Preencher as 2 vagas
        checkin1 = Checkin.objects.create(
            person=self.person1,
            reason='professional',
            active=True
        )
        checkin2 = Checkin.objects.create(
            person=self.person2,
            reason='professional',
            active=True
        )
        
        # Verificar que não há vagas
        self.assertEqual(HouseConfiguration.get_available_vacancies(), 0)
        self.assertTrue(HouseConfiguration.is_at_full_capacity())
        
        # Fazer checkout do primeiro check-in
        checkout_url = '/api/v1/checkouts/'
        checkout_data = {'checkin': checkin1.id}
        checkout_response = self.client.post(checkout_url, checkout_data, format='json')
        
        self.assertEqual(checkout_response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que o checkin foi desativado
        checkin1.refresh_from_db()
        self.assertFalse(checkin1.active)
        
        # Verificar que há 1 vaga disponível agora
        self.assertEqual(HouseConfiguration.get_available_vacancies(), 1)
        self.assertFalse(HouseConfiguration.is_at_full_capacity())
        
        # Verificar que agora é possível fazer novo check-in
        checkin_url = '/api/v1/checkins/'
        checkin_data = {
            'person': self.person3.id,
            'reason': 'professional'
        }
        response = self.client.post(checkin_url, checkin_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Checkin.objects.filter(active=True).count(), 2)
    
    def test_occupancy_calculation(self):
        """
        Teste 4: Verificar se a ocupação é calculada corretamente.
        Esperado: Soma apenas check-ins ativos.
        """
        # Criar 2 check-ins ativos
        Checkin.objects.create(
            person=self.person1,
            reason='professional',
            active=True
        )
        Checkin.objects.create(
            person=self.person2,
            reason='professional',
            active=False  # Inativo
        )
        
        # A ocupação deve ser 1 (apenas ativos)
        self.assertEqual(HouseConfiguration.get_current_occupancy(), 1)
    
    def test_house_configuration_singleton(self):
        """
        Teste 5: Verificar que HouseConfiguration é singleton.
        Esperado: Sempre retorna a mesma instância.
        """
        config1 = HouseConfiguration.get_config()
        config2 = HouseConfiguration.get_config()
        
        self.assertEqual(config1.pk, config2.pk)
        self.assertEqual(config1.pk, 1)
    
    def test_occupancy_status_endpoint(self):
        """
        Teste 6: Verificar se o endpoint de status de ocupação funciona.
        Esperado: Retorna JSON com dados de ocupação.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Criar um check-in
        Checkin.objects.create(
            person=self.person1,
            reason='professional',
            active=True
        )
        
        # Chamar endpoint
        response = self.client.get('/api/v1/house-configuration/occupancy_status/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['max_capacity'], 2)
        self.assertEqual(response.data['current_occupancy'], 1)
        self.assertEqual(response.data['available_vacancies'], 1)
        self.assertFalse(response.data['is_at_full_capacity'])
