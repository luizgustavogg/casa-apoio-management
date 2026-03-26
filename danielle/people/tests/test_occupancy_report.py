from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from people.models import Checkin, Checkout, HouseConfiguration, Person
from people.services import (
    build_occupancy_report,
    build_occupancy_report_xlsx,
    build_typed_report,
)


class OccupancyReportServiceTests(TestCase):
    def setUp(self):
        self.config = HouseConfiguration.get_config()
        self.config.max_capacity = 4
        self.config.save()

        self.person1 = Person.objects.create(name="Person 1")
        self.person2 = Person.objects.create(name="Person 2")

    def test_build_report_with_movement(self):
        checkin1 = Checkin.objects.create(person=self.person1, reason="professional")
        Checkin.objects.filter(pk=checkin1.pk).update(
            created_at=timezone.make_aware(datetime(2026, 3, 10, 10, 0, 0))
        )

        checkin2 = Checkin.objects.create(person=self.person2, reason="professional")
        Checkin.objects.filter(pk=checkin2.pk).update(
            created_at=timezone.make_aware(datetime(2026, 3, 11, 10, 0, 0))
        )

        checkout2 = Checkout.objects.create(checkin=checkin2)
        Checkout.objects.filter(pk=checkout2.pk).update(
            created_at=timezone.make_aware(datetime(2026, 3, 12, 10, 0, 0))
        )

        report = build_occupancy_report(
            start_date=datetime(2026, 3, 10).date(),
            end_date=datetime(2026, 3, 12).date(),
        )

        daily = report["daily"]
        self.assertEqual(len(daily), 3)
        self.assertEqual(daily[0]["occupancy"], 1)  # 10/03
        self.assertEqual(daily[1]["occupancy"], 2)  # 11/03
        self.assertEqual(daily[2]["occupancy"], 1)  # 12/03 (checkout day excluded)

        self.assertEqual(report["capacity"]["peak_occupancy"], 2)
        self.assertEqual(report["capacity"]["lowest_occupancy"], 1)
        self.assertEqual(report["capacity"]["avg_occupancy"], 1.33)

    def test_build_report_with_no_movement(self):
        report = build_occupancy_report(
            start_date=datetime(2026, 4, 1).date(),
            end_date=datetime(2026, 4, 3).date(),
        )

        self.assertEqual(report["period"]["days"], 3)
        self.assertEqual(report["capacity"]["avg_occupancy"], 0)
        self.assertEqual(report["capacity"]["avg_occupancy_rate"], 0)
        self.assertEqual(report["capacity"]["peak_occupancy"], 0)
        self.assertEqual(report["capacity"]["lowest_occupancy"], 0)
        self.assertEqual(len(report["daily"]), 3)

    def test_build_xlsx_report_returns_binary_file(self):
        report = build_typed_report(
            start_date=datetime(2026, 4, 1).date(),
            end_date=datetime(2026, 4, 2).date(),
            report_type="occupancy",
        )

        xlsx_content = build_occupancy_report_xlsx(report)

        # XLSX files are ZIP containers and begin with PK signature.
        self.assertTrue(xlsx_content.startswith(b"PK"))
        self.assertGreater(len(xlsx_content), 1000)

    def test_build_typed_report_for_gender_mix(self):
        report = build_typed_report(
            start_date=datetime(2026, 4, 1).date(),
            end_date=datetime(2026, 4, 3).date(),
            report_type="gender_mix",
        )

        self.assertEqual(report["report_type"], "gender_mix")
        self.assertIn("summary", report)
        self.assertIn("daily", report)
        self.assertEqual(
            report["table"]["keys"], ["date", "male", "female", "other", "total"]
        )
