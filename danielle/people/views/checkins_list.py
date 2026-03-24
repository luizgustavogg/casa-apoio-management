from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Q, Count
from people.models import Checkin, Person
from datetime import datetime


PER_PAGE_OPTIONS = {15, 30, 50}


def _get_per_page(value):
    try:
        per_page = int(value)
    except (TypeError, ValueError):
        return 15
    return per_page if per_page in PER_PAGE_OPTIONS else 15


class CheckinsView(TemplateView):
    template_name = 'checkins.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('q', '').strip()
        per_page = _get_per_page(self.request.GET.get('per_page'))
        
        # Buscar todos os check-ins
        checkins = Checkin.objects.all().select_related('person', 'companion').order_by('-created_at')
        if search_query:
            checkins = checkins.filter(
                Q(person__name__icontains=search_query)
                | Q(companion__name__icontains=search_query)
                | Q(reason__icontains=search_query)
            )
        
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

        paginator = Paginator(checkins, per_page)
        page_obj = paginator.get_page(self.request.GET.get('page'))

        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        pagination_query = query_params.urlencode()
        
        context.update({
            'checkins': page_obj.object_list,
            'page_obj': page_obj,
            'total_checkins': total_checkins,
            'ativos': ativos,
            'inativos': inativos,
            'paciente': paciente,
            'acompanhante': acompanhante,
            'profissional': profissional,
            'voluntario': voluntario,
            'visitante': visitante,
            'outro': outro,
            'search_query': search_query,
            'per_page': per_page,
            'per_page_options': sorted(PER_PAGE_OPTIONS),
            'pagination_query': pagination_query,
        })
        
        return context
