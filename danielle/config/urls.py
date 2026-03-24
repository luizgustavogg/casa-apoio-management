from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from people.views import (UserCreate, CustomObtainAuthToken, UserRetrieve, DashboardView,
                          PessoasView, CheckinsView, HomeServicesView, OccupancyReportView,
                          AuditLogHistoryView)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #path('', admin.site.urls),
    path('admin/', admin.site.urls),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('pessoas', PessoasView.as_view(), name='pessoas'),
    path('checkins', CheckinsView.as_view(), name='checkins'),
    path('home-services', HomeServicesView.as_view(), name='home_services'),
    path('reports', OccupancyReportView.as_view(), name='reports'),
    path('audit-logs', AuditLogHistoryView.as_view(), name='audit_logs'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/', include('people.urls')),
    path('users/', UserCreate.as_view(), name='user_create'),
    path('users/<int:pk>/', UserRetrieve.as_view(), name='user_retrieve'),
    path("login/", CustomObtainAuthToken.as_view(), name="login"),
    path('api-token-auth/', obtain_auth_token, name='api_token_path')
]
