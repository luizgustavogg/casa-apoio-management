from django.test import TestCase

from people.models import AuditLog, Checkin, Checkout, HomeServices, Person


class AuditLogTests(TestCase):
    def setUp(self):
        self.person = Person.objects.create(name="Paciente Auditoria")

    def test_checkin_creation_generates_audit_event(self):
        self.assertEqual(AuditLog.objects.count(), 0)

        checkin = Checkin.objects.create(person=self.person, reason="professional")

        audit = AuditLog.objects.filter(
            action=AuditLog.ACTION_CREATE,
            entity="checkin",
            object_id=checkin.id,
        ).first()

        self.assertIsNotNone(audit)
        self.assertIsNotNone(audit.created_at)
        self.assertIn("reason", audit.changed_fields)
        self.assertEqual(audit.after_data["reason"], "professional")
        self.assertIsNone(audit.before_data)

    def test_home_services_update_generates_field_history(self):
        service = HomeServices.objects.create(person=self.person, lunch=True, dinner=False)

        service.dinner = True
        service.snack = True
        service.save()

        audit = AuditLog.objects.filter(
            action=AuditLog.ACTION_UPDATE,
            entity="homeservices",
            object_id=service.id,
        ).order_by("-id").first()

        self.assertIsNotNone(audit)
        self.assertIn("dinner", audit.changed_fields)
        self.assertIn("snack", audit.changed_fields)
        self.assertEqual(audit.before_data["dinner"], False)
        self.assertEqual(audit.after_data["dinner"], True)
        self.assertEqual(audit.before_data["snack"], False)
        self.assertEqual(audit.after_data["snack"], True)

    def test_checkout_creation_generates_audit_event_with_integrity(self):
        checkin = Checkin.objects.create(person=self.person, reason="patient")

        checkout = Checkout.objects.create(checkin=checkin)

        audit = AuditLog.objects.filter(
            action=AuditLog.ACTION_CREATE,
            entity="checkout",
            object_id=checkout.id,
        ).first()

        self.assertIsNotNone(audit)
        self.assertEqual(audit.after_data["checkin"], checkin.id)
        self.assertIsNone(audit.before_data)
