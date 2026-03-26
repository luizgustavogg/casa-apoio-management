import json
from datetime import datetime

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from people.models import AuditLog
from people.serializers import AuditLogSerializer
from people.services import build_audit_log_xlsx, build_occupancy_report_pdf


PER_PAGE_OPTIONS = {15, 30, 50}
ENTITY_OPTIONS = [
    ("checkin", "Check-ins"),
    ("checkout", "Check-outs"),
    ("homeservices", "Serviços da casa"),
    ("professionalservices", "Serviços profissionais"),
]
IGNORED_EXPORT_FIELDS = {"id", "created_at", "updated_at"}


def _get_per_page(value):
    try:
        per_page = int(value)
    except (TypeError, ValueError):
        return 15
    return per_page if per_page in PER_PAGE_OPTIONS else 15


def _parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date() if value else None
    except ValueError:
        return None


def filter_audit_logs(queryset, params):
    entity = params.get("entity", "").strip()
    action = params.get("action", "").strip()
    start_date = _parse_date(params.get("start_date"))
    end_date = _parse_date(params.get("end_date"))

    if entity:
        queryset = queryset.filter(entity=entity)
    if action:
        queryset = queryset.filter(action=action)
    if start_date:
        queryset = queryset.filter(created_at__date__gte=start_date)
    if end_date:
        queryset = queryset.filter(created_at__date__lte=end_date)

    return queryset


def _pretty_json(value):
    if not value:
        return "—"
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def _compact_value(value):
    if value in (None, "", [], {}):
        return "—"
    if isinstance(value, bool):
        return "Sim" if value else "Não"
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value) or "—"
    if isinstance(value, dict):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    else:
        text = str(value)
    return text if len(text) <= 120 else f"{text[:117]}..."


def _build_field_summary(payload, changed_fields=None):
    if not payload:
        return []

    field_names = changed_fields or list(payload.keys())
    summary = []
    for field_name in field_names:
        if field_name in IGNORED_EXPORT_FIELDS or field_name not in payload:
            continue
        summary.append(
            {
                "field": field_name,
                "value": _compact_value(payload.get(field_name)),
            }
        )

    if not summary:
        for field_name, field_value in payload.items():
            if field_name in IGNORED_EXPORT_FIELDS:
                continue
            summary.append({"field": field_name, "value": _compact_value(field_value)})

    return summary[:12]


def _build_pdf_log_entries(logs):
    entity_labels = dict(ENTITY_OPTIONS)
    entries = []

    for log in logs:
        relevant_fields = [
            field_name
            for field_name in (log.changed_fields or [])
            if field_name not in IGNORED_EXPORT_FIELDS
        ]
        summary_fields = (
            relevant_fields if log.action == AuditLog.ACTION_UPDATE else None
        )

        entries.append(
            {
                "created_at": log.created_at,
                "action_label": log.get_action_display(),
                "entity_label": entity_labels.get(log.entity, log.entity),
                "entity": log.entity,
                "object_id": log.object_id,
                "changed_fields": relevant_fields,
                "before_summary": _build_field_summary(log.before_data, summary_fields),
                "after_summary": _build_field_summary(log.after_data, summary_fields),
            }
        )

    return entries


def _annotate_logs(logs):
    for log in logs:
        log.before_data_pretty = _pretty_json(log.before_data)
        log.after_data_pretty = _pretty_json(log.after_data)
    return logs


def _build_filter_summary(params):
    entity = params.get("entity", "") or "Todas as entidades"
    action = params.get("action", "") or "Todas as ações"
    start_date = params.get("start_date", "") or "início"
    end_date = params.get("end_date", "") or "hoje"
    return f"Filtros: entidade={entity} | ação={action} | período={start_date} até {end_date}"


def _build_pdf_response(logs, params):
    logs = list(logs)
    context = {
        "logs": _build_pdf_log_entries(logs),
        "total_logs": len(logs),
        "filter_summary": _build_filter_summary(params),
    }
    pdf_html = render_to_string("audit_logs_pdf.html", context)
    pdf_content = build_occupancy_report_pdf(pdf_html)
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=audit_logs.pdf"
    return response


def _build_xlsx_response(logs, params):
    xlsx_content = build_audit_log_xlsx(
        logs, filter_summary=_build_filter_summary(params)
    )
    response = HttpResponse(
        xlsx_content,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=audit_logs.xlsx"
    return response


class AuditLogHistoryView(TemplateView):
    template_name = "audit_logs.html"

    def get(self, request, *args, **kwargs):
        filtered_logs = filter_audit_logs(AuditLog.objects.all(), request.GET)
        export = request.GET.get("export")

        if export == "pdf":
            return _build_pdf_response(filtered_logs, request.GET)

        if export == "xlsx":
            return _build_xlsx_response(filtered_logs, request.GET)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_logs = filter_audit_logs(AuditLog.objects.all(), self.request.GET)
        per_page = _get_per_page(self.request.GET.get("per_page"))

        paginator = Paginator(filtered_logs, per_page)
        page_obj = paginator.get_page(self.request.GET.get("page"))

        _annotate_logs(page_obj.object_list)

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        pagination_query = query_params.urlencode()

        context.update(
            {
                "logs": page_obj.object_list,
                "page_obj": page_obj,
                "pagination_query": pagination_query,
                "per_page": per_page,
                "per_page_options": sorted(PER_PAGE_OPTIONS),
                "entity_options": ENTITY_OPTIONS,
                "action_options": AuditLog.ACTION_CHOICES,
                "selected_entity": self.request.GET.get("entity", ""),
                "selected_action": self.request.GET.get("action", ""),
                "start_date": self.request.GET.get("start_date", ""),
                "end_date": self.request.GET.get("end_date", ""),
                "total_logs": filtered_logs.count(),
                "created_count": filtered_logs.filter(
                    action=AuditLog.ACTION_CREATE
                ).count(),
                "updated_count": filtered_logs.filter(
                    action=AuditLog.ACTION_UPDATE
                ).count(),
                "deleted_count": filtered_logs.filter(
                    action=AuditLog.ACTION_DELETE
                ).count(),
            }
        )
        return context


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "entity", "action", "object_id"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return filter_audit_logs(queryset, self.request.query_params)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        export = request.query_params.get("export")

        if export == "pdf":
            return _build_pdf_response(queryset, request.query_params)

        if export == "xlsx":
            return _build_xlsx_response(queryset, request.query_params)

        return super().list(request, *args, **kwargs)
