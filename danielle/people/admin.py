from django.contrib import admin
from people.models import Checkin
from people.models import Person
from people.models import Checkout
from people.models import HomeServices
from people.models import ProfessionalServices

admin.site.site_header = "Gestão de pessoas"
admin.site.site_title = "Gestão fácil!"
admin.site.index_title = "Bem vindo! "


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'born_date')
    list_filter = ['gender', 'state']
    search_fields = ['name']
    fieldsets = [('Identificação', {
        'fields': [
            'name', 'mother_name', 'born_date', 'cpf', ('rg', 'rg_ssp'),
            'gender'
        ]
    }),
                 ('Endereço', {
                     'fields': [
                         'address_line_1', 'address_line_2', 'neighbourhood',
                         'state', 'city', 'postal_code', 'residence_type'
                     ]
                 }),
                 ('Contato', {
                     'fields': [
                         'email', ('ddd_private_phone', 'private_phone'),
                         ('ddd_message_phone', 'message_phone')
                     ]
                 }),
                 ('Outras informações', {
                     'fields': ['observation', 'death_date'],
                     'classes': ('collapse', ),
                 })]


class CheckinAdmin(admin.ModelAdmin):
    list_display = ('person', 'reason', 'created_at')
    list_filter = ['reason']
    search_fields = ['person']
    fieldsets = [('Identificação', {
        'fields': ['person', 'reason']
    }),
                 ('Preencher se paciente:', {
                     'fields': [
                         'companion',
                         ('chemotherapy', 'radiotherapy', 'surgery',
                          'appointment', 'exams', 'other'), 'ca_number',
                         'social_vacancy'
                     ]
                 }),
                 ('Outras informações', {
                     'fields': ['observation', 'active'],
                     'classes': ('collapse', ),
                 })]


class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('checkin', 'created_at')


class HomeServicesAdmin(admin.ModelAdmin):
    list_display = ('person', 'breakfast', 'lunch', 'snack', 'dinner',
                    'shower', 'sleep', 'created_at')


class ProfessionalServicesAdmin(admin.ModelAdmin):
    list_display = ('professional', 'title', 'description', 'created_at')


admin.site.register(Person, PersonAdmin)
admin.site.register(Checkin, CheckinAdmin)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(HomeServices, HomeServicesAdmin)
admin.site.register(ProfessionalServices, ProfessionalServicesAdmin)
