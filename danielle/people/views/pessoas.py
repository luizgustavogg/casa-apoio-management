from django.views.generic import TemplateView
from django.db.models import Count, Q
from people.models import Person


class PessoasView(TemplateView):
    template_name = 'pessoas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('q', '').strip()
        
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
        
        context.update({
            'pessoas': pessoas,
            'total_pessoas': total_pessoas,
            'masculino': masculino,
            'feminino': feminino,
            'outro': outro,
            'search_query': search_query,
        })
        
        return context
