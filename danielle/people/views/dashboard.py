from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from people.models import Person, Checkin, HomeServices
import json


class DashboardView(TemplateView):
    """
    View que renderiza o dashboard com indicadores da casa de apoio.
    Acessível sem autenticação.
    """

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Contadores gerais
        total_people = Person.objects.count()
        total_active_checkins = Checkin.objects.filter(active=True).count()
        total_checkins = Checkin.objects.count()
        
        # Taxa de ocupação estimada
        occupation_rate = (
            (total_active_checkins / max(total_people, 1)) * 100
            if total_people > 0
            else 0
        )

        # Distribuição por gênero
        gender_distribution = (
            Person.objects.values("gender")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Tipos de check-in
        checkin_reasons = (
            Checkin.objects.values("reason")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Casos de tratamento (apenas check-ins ativos)
        active_checkins = Checkin.objects.filter(active=True)

        treatment_data = {
            "chemotherapy": active_checkins.filter(chemotherapy=True).count(),
            "radiotherapy": active_checkins.filter(radiotherapy=True).count(),
            "surgery": active_checkins.filter(surgery=True).count(),
            "exams": active_checkins.filter(exams=True).count(),
            "appointment": active_checkins.filter(appointment=True).count(),
            "other": active_checkins.filter(other=True).count(),
        }

        # Calcular o máximo para a barra de progresso
        max_treatment = max(treatment_data.values()) if treatment_data.values() else 1

        # Adicionar percentuais
        treatment_with_percentage = []
        for key, count in treatment_data.items():
            percentage = (count / max_treatment * 100) if max_treatment > 0 else 0
            treatment_labels = {
                "chemotherapy": ("Quimioterapia", "bi-capsule"),
                "radiotherapy": ("Radioterapia", "bi-radioactive"),
                "surgery": ("Cirurgia", "bi-bandaid"),
                "exams": ("Exames", "bi-hospital"),
                "appointment": ("Consultas", "bi-calendar-check"),
                "other": ("Outros", "bi-question-circle"),
            }
            label, icon = treatment_labels[key]
            treatment_with_percentage.append({
                "key": key,
                "label": label,
                "icon": icon,
                "count": count,
                "percentage": int(percentage)
            })

        # Serviços da casa (últimas semanas - pessoas ativas)
        home_services_count = HomeServices.objects.filter(
            person_id__in=Checkin.objects.filter(active=True).values_list(
                "person_id", flat=True
            )
        ).count()

        # Vagas sociais
        social_vacancies = Checkin.objects.filter(
            active=True, social_vacancy=True
        ).count()
        
        # Dados para gráfico de tipo de check-in por dia (últimos 7 dias)
        seven_days_ago = timezone.now() - timedelta(days=7)
        daily_checkins = []
        labels_7days = []
        
        for i in range(6, -1, -1):
            date = timezone.now().date() - timedelta(days=i)
            count = Checkin.objects.filter(
                created_at__date=date
            ).count()
            daily_checkins.append(count)
            labels_7days.append(date.strftime("%d/%m"))
        
        # Distribuição dos tipos de check-in para gráfico
        checkin_labels = []
        checkin_data = []
        colors_checkin = [
            '#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#1abc9c'
        ]
        
        for idx, item in enumerate(checkin_reasons):
            reason_map = {
                'patient': '👤 Paciente',
                'companion': '👥 Acompanhante',
                'professional': '👨‍⚕️ Profissional',
                'voluntary': '🤝 Voluntário',
                'visitor': '🚶 Visitante',
                'other': '❓ Outro'
            }
            checkin_labels.append(reason_map.get(item['reason'], item['reason']))
            checkin_data.append(item['count'])

        context.update(
            {
                "total_people": total_people,
                "total_active_checkins": total_active_checkins,
                "total_checkins": total_checkins,
                "occupation_rate": int(occupation_rate),
                "gender_distribution": list(gender_distribution),
                "checkin_reasons": list(checkin_reasons),
                "treatment_data": treatment_with_percentage,
                "home_services_count": home_services_count,
                "social_vacancies": social_vacancies,
                "daily_checkins_labels": json.dumps(labels_7days),
                "daily_checkins_data": json.dumps(daily_checkins),
                "checkin_labels": json.dumps(checkin_labels),
                "checkin_data": json.dumps(checkin_data),
                "colors_checkin": json.dumps(colors_checkin),
                "treatment_counts": json.dumps([item['count'] for item in treatment_with_percentage]),
                "treatment_labels": json.dumps([item['label'] for item in treatment_with_percentage]),
            }
        )

        return context
