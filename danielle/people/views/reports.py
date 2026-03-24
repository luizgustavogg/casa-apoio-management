from datetime import datetime, timedelta
import json

from django.http import HttpResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from people.services import (
    build_occupancy_report_pdf,
    build_occupancy_report_xlsx,
    build_typed_report,
    get_report_type_options,
)


PER_PAGE_OPTIONS = {15, 30, 50}


def _parse_period(start_value, end_value):
    today = datetime.now().date()
    default_start = today - timedelta(days=29)

    try:
        start_date = datetime.strptime(start_value, "%Y-%m-%d").date() if start_value else default_start
    except ValueError:
        start_date = default_start

    try:
        end_date = datetime.strptime(end_value, "%Y-%m-%d").date() if end_value else today
    except ValueError:
        end_date = today

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    return start_date, end_date


def _normalize_report_type(report_type):
    valid_types = {value for value, _ in get_report_type_options()}
    return report_type if report_type in valid_types else "occupancy"


def _get_per_page(value):
    try:
        per_page = int(value)
    except (TypeError, ValueError):
        return 15
    return per_page if per_page in PER_PAGE_OPTIONS else 15


def _build_report_context(start_date, end_date, report_data, report_type):
    chart_datasets = report_data.get("chart", {}).get("datasets", [])
    chart_labels = [item["date"] for item in report_data.get("daily", [])]

    return {
        "report_data": report_data,
        "report_type": report_type,
        "report_type_options": get_report_type_options(),
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily_labels": json.dumps(chart_labels),
        "chart_datasets": json.dumps(chart_datasets),
        "chart_y_axis_label": report_data.get("chart", {}).get("y_axis_label", "Valor"),
        "chart_max_hint": report_data.get("chart", {}).get("max_value_hint", 0),
    }


def _build_pdf_response(start_date, end_date, report_data, report_type):
    context = _build_report_context(start_date, end_date, report_data, report_type)
    pdf_html = render_to_string("reports_pdf.html", context)
    pdf_content = build_occupancy_report_pdf(pdf_html)
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = (
        f"attachment; filename=report_{report_type}_{start_date}_{end_date}.pdf"
    )
    return response


def _build_xlsx_response(start_date, end_date, report_data, report_type):
    xlsx_content = build_occupancy_report_xlsx(report_data)
    response = HttpResponse(
        xlsx_content,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = (
        f"attachment; filename=report_{report_type}_{start_date}_{end_date}.xlsx"
    )
    return response


class OccupancyReportView(TemplateView):
    template_name = "reports.html"

    def get(self, request, *args, **kwargs):
        start_raw = request.GET.get("start_date")
        end_raw = request.GET.get("end_date")
        report_type = _normalize_report_type(request.GET.get("report_type", "occupancy"))
        per_page = _get_per_page(request.GET.get("per_page"))
        export = request.GET.get("export")

        start_date, end_date = _parse_period(start_raw, end_raw)
        report_data = build_typed_report(start_date, end_date, report_type=report_type)

        if export == "pdf":
            return _build_pdf_response(start_date, end_date, report_data, report_type)

        if export == "xlsx":
            return _build_xlsx_response(start_date, end_date, report_data, report_type)

        daily_paginator = Paginator(report_data.get("daily", []), per_page)
        page_obj = daily_paginator.get_page(request.GET.get("page"))
        report_data = {
            **report_data,
            "daily": list(page_obj.object_list),
        }

        query_params = request.GET.copy()
        query_params.pop("page", None)
        pagination_query = query_params.urlencode()

        context = self.get_context_data(
            **_build_report_context(start_date, end_date, report_data, report_type)
        )
        context["page_obj"] = page_obj
        context["per_page"] = per_page
        context["per_page_options"] = sorted(PER_PAGE_OPTIONS)
        context["pagination_query"] = pagination_query
        return self.render_to_response(context)


class OccupancyReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_raw = request.GET.get("start_date")
        end_raw = request.GET.get("end_date")
        report_type = _normalize_report_type(request.GET.get("report_type", "occupancy"))
        export = request.GET.get("export")

        start_date, end_date = _parse_period(start_raw, end_raw)
        report_data = build_typed_report(start_date, end_date, report_type=report_type)

        if export == "pdf":
            return _build_pdf_response(start_date, end_date, report_data, report_type)

        if export == "xlsx":
            return _build_xlsx_response(start_date, end_date, report_data, report_type)

        return Response(report_data)
