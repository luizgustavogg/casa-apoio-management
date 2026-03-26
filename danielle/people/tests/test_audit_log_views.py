from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from people.models import AuditLog, Checkin, Checkout, HomeServices, Person


class AuditLogAPIViewTests(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.person = Person.objects.create(name="Auditoria API")
        self.checkin = Checkin.objects.create(person=self.person, reason="patient")
        self.checkout = Checkout.objects.create(checkin=self.checkin)
        self.service = HomeServices.objects.create(person=self.person, dinner=True)
        self.service.lunch = True
        self.service.save()

        old_date = timezone.now() - timedelta(days=10)
        AuditLog.objects.filter(entity="checkin", action="create").update(
            created_at=old_date
        )

    @staticmethod
    def setup_user():
        user_model = get_user_model()
        return user_model.objects.create_user(
            "audit-api",
            email="audit-api@test.com",
            password="test",
        )

    def test_list_audit_logs_with_entity_and_action_filters(self):
        response = self.client.get("/api/v1/audit-logs/?entity=checkout&action=create")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["entity"], "checkout")
        self.assertEqual(response.data["results"][0]["action"], "create")

    def test_list_audit_logs_with_date_range_filters(self):
        start_date = (timezone.now() - timedelta(days=2)).date().isoformat()
        end_date = timezone.now().date().isoformat()

        response = self.client.get(
            f"/api/v1/audit-logs/?start_date={start_date}&end_date={end_date}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data["count"], 2)
        for item in response.data["results"]:
            self.assertNotEqual(item["entity"], "checkin")

    def test_export_audit_logs_as_xlsx(self):
        response = self.client.get("/api/v1/audit-logs/?entity=checkout&export=xlsx")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertTrue(response.content.startswith(b"PK"))

    def test_export_audit_logs_as_pdf(self):
        response = self.client.get("/api/v1/audit-logs/?action=create&export=pdf")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertGreater(len(response.content), 100)


class AuditLogHistoryViewTests(TestCase):
    def setUp(self):
        person = Person.objects.create(name="Auditoria Tela")
        checkin = Checkin.objects.create(person=person, reason="professional")
        checkin.reason = "visitor"
        checkin.save()

    def test_audit_history_page_renders_and_filters(self):
        response = self.client.get(
            "/audit-logs", {"entity": "checkin", "action": "update"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Histórico de Alterações")
        self.assertContains(response, "checkin")

    def test_audit_history_page_exports_pdf(self):
        response = self.client.get(
            "/audit-logs", {"entity": "checkin", "export": "pdf"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
