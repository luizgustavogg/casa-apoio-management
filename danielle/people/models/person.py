from django.db import models
from utils.cep.check_cep import check_cep

from utils.city.check_city import check_city
from utils.cpf.check_cpf import check_cpf
from utils.phone.check_phone import check_phone

from .base import BaseModel


class Person(BaseModel):
    class Meta:
        verbose_name_plural = "Pessoas"
        verbose_name = "Pessoa"

    name = models.CharField(max_length=100, verbose_name='Nome')
    mother_name = models.CharField(max_length=100,
                                   blank=True,
                                   null=True,
                                   verbose_name='Nome da mãe')
    born_date = models.DateField(blank=True,
                                 null=True,
                                 help_text="Exemplo: 03/12/2015",
                                 verbose_name='Dt. nascimento')
    death_date = models.DateField(blank=True,
                                  null=True,
                                  verbose_name='Dt. óbito')
    email = models.EmailField(max_length=100,
                              blank=True,
                              null=True,
                              unique=True,
                              verbose_name='E-mail')
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              blank=True,
                              null=True,
                              verbose_name='Gênero')
    cpf = models.CharField(max_length=14,
                           blank=True,
                           null=True,
                           unique=True,
                           help_text='Exemplo: 00000000000',
                           verbose_name='CPF',
                           validators=[check_cpf])
    STATE_CHOICES = [("SP", "São Paulo"), ("PR", "Paraná"),
                     ("SC", "Santa Catarina"), ("RS", "Rio Grande do Sul"),
                     ("MS", "Mato Grosso do Sul"), ("RO", "Rondônia"),
                     ("AC", "Acre"), ("AM", "Amazonas"), ("RR", "Roraima"),
                     ("PA", "Pará"), ("AP", "Amapá"), ("TO", "Tocantins"),
                     ("MA", "Maranhão"), ("RN", "Rio Grande do Norte"),
                     ("PB", "Paraíba"), ("PE", "Pernambuco"),
                     ("AL", "Alagoas"), ("SE", "Sergipe"), ("BA", "Bahia"),
                     ("MG", "Minas Gerais"), ("RJ", "Rio de Janeiro"),
                     ("MT", "Mato Grosso"), ("GO", "Goiás"),
                     ("DF", "Distrito Federal"), ("PI", "Piauí"),
                     ("CE", "Ceará"), ("ES", "Espírito Santo")]
    rg = models.CharField(max_length=14,
                          blank=True,
                          null=True,
                          verbose_name='RG')
    rg_ssp = models.CharField(max_length=2,
                              choices=STATE_CHOICES,
                              blank=True,
                              null=True,
                              verbose_name='SSP')
    state = models.CharField(max_length=2,
                             choices=STATE_CHOICES,
                             blank=True,
                             null=True,
                             verbose_name='Estado')
    address_line_1 = models.CharField(max_length=100,
                                      blank=True,
                                      null=True,
                                      help_text='Rua e número da residência',
                                      verbose_name='Endereço (linha 1)')
    address_line_2 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Complemento (apartamento, bloco,...)',
        verbose_name='Endereço (linha 2)')
    neighbourhood = models.CharField(max_length=60,
                                     blank=True,
                                     null=True,
                                     verbose_name='Bairro')
    city = models.CharField(max_length=60,
                            blank=True,
                            null=True,
                            verbose_name="Cidade",
                            validators=[check_city])
    postal_code = models.CharField(max_length=15,
                                   blank=True,
                                   null=True,
                                   help_text='Exemplo: 00000000',
                                   verbose_name="CEP",
                                   validators=[check_cep])
    RESIDENCE_TYPE_CHOICES = [('urban', 'Urbano'), ('rural', 'Rural')]
    residence_type = models.CharField(max_length=6,
                                      choices=RESIDENCE_TYPE_CHOICES,
                                      blank=True,
                                      null=True,
                                      verbose_name='Distrito')
    DDD_CHOICES = [('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
                   ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'),
                   ('19', '19'), ('21', '21'), ('22', '22'), ('24', '24'),
                   ('27', '27'), ('28', '28'), ('31', '31'), ('32', '32'),
                   ('33', '33'), ('34', '34'), ('35', '35'), ('37', '37'),
                   ('38', '38'), ('41', '41'), ('42', '42'), ('43', '43'),
                   ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'),
                   ('48', '48'), ('49', '49'), ('51', '51'), ('53', '53'),
                   ('54', '54'), ('55', '55'), ('61', '61'), ('62', '62'),
                   ('63', '63'), ('64', '64'), ('65', '65'), ('66', '66'),
                   ('67', '67'), ('68', '68'), ('69', '69'), ('71', '71'),
                   ('73', '73'), ('74', '74'), ('75', '75'), ('77', '77'),
                   ('79', '79'), ('81', '81'), ('82', '82'), ('83', '83'),
                   ('84', '84'), ('85', '85'), ('86', '86'), ('87', '87'),
                   ('88', '88'), ('89', '89'), ('91', '91'), ('92', '92'),
                   ('93', '93'), ('94', '94'), ('95', '95'), ('96', '96'),
                   ('97', '97'), ('98', '98'), ('99', '99')]

    ddd_private_phone = models.CharField(max_length=2,
                                         blank=True,
                                         null=True,
                                         choices=DDD_CHOICES,
                                         help_text="Apenas 2 dígitos",
                                         verbose_name="DDD")
    private_phone = models.CharField(max_length=10,
                                     blank=True,
                                     null=True,
                                     help_text='Exemplo: 999999999',
                                     verbose_name='Tel. p/ contato',
                                     validators=[check_phone])
    ddd_message_phone = models.CharField(max_length=2,
                                         blank=True,
                                         null=True,
                                         choices=DDD_CHOICES,
                                         help_text="Apenas 2 dígitos",
                                         verbose_name="DDD")
    message_phone = models.CharField(max_length=10,
                                     blank=True,
                                     null=True,
                                     help_text='Exemplo: 999999999',
                                     verbose_name='Tel. p/ mensagem',
                                     validators=[check_phone])
    observation = models.TextField(max_length=600,
                                   blank=True,
                                   null=True,
                                   verbose_name='Observação')

    @property
    def formatted_born_date(self):
        if self.born_date:
            return self.born_date.strftime("%d/%m/%Y")

    @property
    def formatted_death_date(self):
        if self.death_date:
            return self.death_date.strftime("%d/%m/%Y")

    @property
    def formatted_cpf(self):
        if self.cpf:
            return "{}.{}.{}-{}".format(self.cpf[:3], self.cpf[3:6],
                                        self.cpf[6:9], self.cpf[9:11])

    @property
    def formatted_postal_code(self):
        if self.postal_code:
            return "{}-{}".format(self.postal_code[:5], self.postal_code[5:9])

    def __str__(self):
        return self.name
