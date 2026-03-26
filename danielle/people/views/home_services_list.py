from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Count, Q
from people.models import HomeServices, Person


PER_PAGE_OPTIONS = {15, 30, 50}


def _get_per_page(value):
    try:
        per_page = int(value)
    except (TypeError, ValueError):
        return 15
    return per_page if per_page in PER_PAGE_OPTIONS else 15


class HomeServicesView(TemplateView):
    template_name = "home_services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get("q", "").strip()
        per_page = _get_per_page(self.request.GET.get("per_page"))

        # Buscar todos os serviços
        servicos = (
            HomeServices.objects.all().select_related("person").order_by("-created_at")
        )
        if search_query:
            servicos = servicos.filter(person__name__icontains=search_query)

        # Estatísticas
        total_servicos = servicos.count()
        cafe_manha = servicos.filter(breakfast=True).count()
        almoco = servicos.filter(lunch=True).count()
        lanche = servicos.filter(snack=True).count()
        jantar = servicos.filter(dinner=True).count()
        banho = servicos.filter(shower=True).count()
        pernoite = servicos.filter(sleep=True).count()

        paginator = Paginator(servicos, per_page)
        page_obj = paginator.get_page(self.request.GET.get("page"))

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        pagination_query = query_params.urlencode()

        context.update(
            {
                "servicos": page_obj.object_list,
                "page_obj": page_obj,
                "total_servicos": total_servicos,
                "cafe_manha": cafe_manha,
                "almoco": almoco,
                "lanche": lanche,
                "jantar": jantar,
                "banho": banho,
                "pernoite": pernoite,
                "search_query": search_query,
                "per_page": per_page,
                "per_page_options": sorted(PER_PAGE_OPTIONS),
                "pagination_query": pagination_query,
            }
        )

        return context
