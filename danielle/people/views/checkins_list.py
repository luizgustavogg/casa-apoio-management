from django.views.generic import TemplateView
from django.db.models import Q, Count
from people.models import Checkin, Person
from datetime import datetime


class CheckinsView(TemplateView):
    template_name = 'checkins.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar todos os check-ins
        checkins = Checkin.objects.all().select_related('person', 'companion').order_by('-created_at')
        
        # Estatísticas
        total_checkins = checkins.count()
        ativos = checkins.filter(active=True).count()
        inativos = checkins.filter(active=False).count()
        
        # Distribuição por tipo
        paciente = checkins.filter(reason='patient').count()
        acompanhante = checkins.filter(reason='companion').count()
        profissional = checkins.filter(reason='professional').count()
        voluntario = checkins.filter(reason='voluntary').count()
        visitante = checkins.filter(reason='visitor').count()
        outro = checkins.filter(reason='other').count()
        
        context.update({
            'checkins': checkins[:100],  # Limitar a 100 para não sobrecarregar
            'total_checkins': total_checkins,
            'ativos': ativos,
            'inativos': inativos,
            'paciente': paciente,
            'acompanhante': acompanhante,
            'profissional': profissional,
            'voluntario': voluntario,
            'visitante': visitante,
            'outro': outro,
        })
        
        return context
