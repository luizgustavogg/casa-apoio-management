from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Count, Q
from people.models import Person


PER_PAGE_OPTIONS = {15, 30, 50}


def _get_per_page(value):
    try:
        per_page = int(value)
    except (TypeError, ValueError):
        return 15
    return per_page if per_page in PER_PAGE_OPTIONS else 15


class PessoasView(TemplateView):
    template_name = 'pessoas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('q', '').strip()
        per_page = _get_per_page(self.request.GET.get('per_page'))
        
        # Buscar todas as pessoas
        pessoas = Person.objects.all().order_by('-created_at')
        if search_query:
            pessoas = pessoas.filter(
                Q(name__icontains=search_query)
                | Q(cpf__icontains=search_query)
                | Q(email__icontains=search_query)
            )
        
        # Estatísticas
        total_pessoas = pessoas.count()
        masculino = pessoas.filter(gender='M').count()
        feminino = pessoas.filter(gender='F').count()
        outro = pessoas.filter(gender='O').count()

        paginator = Paginator(pessoas, per_page)
        page_obj = paginator.get_page(self.request.GET.get('page'))

        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        pagination_query = query_params.urlencode()
        
        context.update({
            'pessoas': page_obj.object_list,
            'page_obj': page_obj,
            'total_pessoas': total_pessoas,
            'masculino': masculino,
            'feminino': feminino,
            'outro': outro,
            'search_query': search_query,
            'per_page': per_page,
            'per_page_options': sorted(PER_PAGE_OPTIONS),
            'pagination_query': pagination_query,
        })
        
        return context
