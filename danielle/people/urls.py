from django.urls import path, include
from people import views

# ViewSet class based views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('people', views.PersonViewSet)
router.register('checkins', views.CheckinViewSet)
router.register('patient_companion_checkin',
                views.PatientCompanionCheckinViewSet)
router.register('home_services', views.HomeServicesViewSet)
router.register('professional_services', views.ProfessionalServicesViewSet)
# router.register('checkins', views.CheckinViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
