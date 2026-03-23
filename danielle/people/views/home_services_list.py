from django.views.generic import TemplateView
from django.db.models import Count, Q
from people.models import HomeServices, Person


class HomeServicesView(TemplateView):
    template_name = 'home_services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar todos os serviços
        servicos = HomeServices.objects.all().select_related('person').order_by('-created_at')
        
        # Estatísticas
        total_servicos = servicos.count()
        cafe_manha = servicos.filter(breakfast=True).count()
        almoco = servicos.filter(lunch=True).count()
        lanche = servicos.filter(snack=True).count()
        jantar = servicos.filter(dinner=True).count()
        banho = servicos.filter(shower=True).count()
        pernoite = servicos.filter(sleep=True).count()
        
        context.update({
            'servicos': servicos[:100],  # Limitar a 100 para não sobrecarregar
            'total_servicos': total_servicos,
            'cafe_manha': cafe_manha,
            'almoco': almoco,
            'lanche': lanche,
            'jantar': jantar,
            'banho': banho,
            'pernoite': pernoite,
        })
        
        return context
