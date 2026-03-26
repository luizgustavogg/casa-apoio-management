from django.urls import path, include
from people import views

# ViewSet class based views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("people", views.PersonViewSet)
router.register("checkins", views.CheckinViewSet)
router.register("checkouts", views.CheckoutViewSet)
router.register("house-configuration", views.HouseConfigurationViewSet)
router.register("patient_companion_checkin", views.PatientCompanionCheckinViewSet)
router.register("home_services", views.HomeServicesViewSet)
router.register("professional_services", views.ProfessionalServicesViewSet)
router.register("audit-logs", views.AuditLogViewSet, basename="audit-log")
# router.register('checkins', views.CheckinViewSet)

urlpatterns = [
    path(
        "reports/occupancy/",
        views.OccupancyReportAPIView.as_view(),
        name="occupancy_report_api",
    ),
    path("", include(router.urls)),
]
