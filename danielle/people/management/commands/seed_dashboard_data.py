import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from people.models import Checkin, Checkout, HomeServices, HouseConfiguration, Person


FIRST_NAMES = [
    "Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena",
    "Igor", "Juliana", "Kaique", "Larissa", "Marcos", "Natália", "Otávio", "Patrícia",
    "Rafael", "Sabrina", "Tiago", "Vanessa", "William", "Yasmin", "Diego", "Camila",
]

LAST_NAMES = [
    "Silva", "Souza", "Oliveira", "Santos", "Lima", "Costa", "Pereira", "Rodrigues",
    "Almeida", "Nunes", "Barbosa", "Melo", "Araújo", "Mendes", "Carvalho", "Teixeira",
]

CITIES = [
    "Curitiba", "Ponta Grossa", "Londrina", "Maringá", "Cascavel", "Foz do Iguaçu", "Guarapuava",
]


class Command(BaseCommand):
    help = "Popula o banco com dados variados e realistas para o dashboard."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Remove dados de pessoas/check-ins/check-outs/serviços antes de popular.",
        )
        parser.add_argument(
            "--people",
            type=int,
            default=80,
            help="Quantidade de pessoas para criar (padrao: 80).",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=45,
            help="Janela de dias para distribuir eventos (padrao: 45).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(20260324)

        people_count = max(20, int(options["people"]))
        days_window = max(14, int(options["days"]))

        if options["reset"]:
            self.stdout.write("Limpando dados anteriores...")
            Checkout.objects.all().delete()
            HomeServices.objects.all().delete()
            Checkin.objects.all().delete()

        config = HouseConfiguration.get_config()
        if config.max_capacity < 25:
            config.max_capacity = 30
            config.save()

        existing_people_count = Person.objects.count()
        missing_people = max(0, people_count - existing_people_count)
        if missing_people > 0:
            self._create_people(missing_people)

        people = list(Person.objects.all())
        checkins = self._create_checkins(people, days_window)
        self._create_checkouts(checkins)
        self._create_home_services(checkins, days_window)

        now = timezone.now()
        last_7_days = now - timedelta(days=7)
        prev_7_days = now - timedelta(days=14)

        active_checkins = Checkin.objects.filter(active=True).count()
        total_checkins = Checkin.objects.count()
        total_checkouts = Checkout.objects.count()
        total_services = HomeServices.objects.count()
        new_checkins_7d = Checkin.objects.filter(created_at__gte=last_7_days).count()
        prev_checkins_7d = Checkin.objects.filter(
            created_at__gte=prev_7_days,
            created_at__lt=last_7_days,
        ).count()

        capacity_rate = (active_checkins / config.max_capacity * 100) if config.max_capacity else 0

        self.stdout.write(self.style.SUCCESS("\nSeed concluido com sucesso."))
        self.stdout.write(f"Pessoas: {Person.objects.count()}")
        self.stdout.write(f"Check-ins totais: {total_checkins}")
        self.stdout.write(f"Check-ins ativos: {active_checkins}")
        self.stdout.write(f"Check-outs: {total_checkouts}")
        self.stdout.write(f"Servicos da casa: {total_services}")
        self.stdout.write(f"Novos check-ins (7 dias): {new_checkins_7d}")
        self.stdout.write(f"Check-ins 7 dias anteriores: {prev_checkins_7d}")
        self.stdout.write(f"Capacidade maxima: {config.max_capacity}")
        self.stdout.write(f"Taxa de ocupacao atual: {capacity_rate:.1f}%")

    def _create_people(self, people_count):
        people = []
        for index in range(people_count):
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            name = f"{first} {last} {index + 1}"
            gender = random.choices(["M", "F", "O"], weights=[0.47, 0.48, 0.05], k=1)[0]

            person = Person.objects.create(
                name=name,
                gender=gender,
                email=f"demo.person.{index + 1}@example.com",
                city=random.choice(CITIES),
                state="PR",
                residence_type=random.choice(["urban", "rural"]),
            )

            created_at = self._random_datetime_within_days(120)
            Person.objects.filter(pk=person.pk).update(created_at=created_at, updated_at=created_at)
            person.created_at = created_at
            people.append(person)

        return people

    def _create_checkins(self, people, days_window):
        checkins = []
        reasons = ["patient", "companion", "professional", "voluntary", "visitor", "other"]
        reason_weights = [0.42, 0.12, 0.20, 0.10, 0.10, 0.06]

        total_checkins_to_create = max(int(len(people) * 1.1), 55)

        for _ in range(total_checkins_to_create):
            person = random.choice(people)
            reason = random.choices(reasons, weights=reason_weights, k=1)[0]
            companion = None

            if reason == "companion":
                companion_candidates = [candidate for candidate in people if candidate.id != person.id]
                if companion_candidates:
                    companion = random.choice(companion_candidates)

            treatment_probability = 0.7 if reason == "patient" else 0.22
            chemotherapy = random.random() < (0.28 if reason == "patient" else 0.03)
            radiotherapy = random.random() < (0.24 if reason == "patient" else 0.02)
            surgery = random.random() < (0.18 if reason == "patient" else 0.02)
            exams = random.random() < (0.32 if reason == "patient" else 0.04)
            appointment = random.random() < (0.39 if reason == "patient" else 0.06)
            other_treatment = random.random() < (0.08 if reason == "patient" else 0.03)

            if random.random() < treatment_probability and not any(
                [chemotherapy, radiotherapy, surgery, exams, appointment, other_treatment]
            ):
                appointment = True

            social_vacancy = None
            if reason in {"patient", "companion"}:
                social_vacancy = random.random() < 0.28

            checkin = Checkin.objects.create(
                person=person,
                reason=reason,
                companion=companion,
                chemotherapy=chemotherapy,
                radiotherapy=radiotherapy,
                surgery=surgery,
                exams=exams,
                appointment=appointment,
                other=other_treatment,
                social_vacancy=social_vacancy,
                active=True,
            )

            created_at = self._random_datetime_within_days(days_window)
            Checkin.objects.filter(pk=checkin.pk).update(created_at=created_at, updated_at=created_at)
            checkin.created_at = created_at
            checkins.append(checkin)

        return checkins

    def _create_checkouts(self, checkins):
        if not checkins:
            return

        config = HouseConfiguration.get_config()
        target_active = max(8, int(config.max_capacity * 0.72))

        ordered_checkins = sorted(checkins, key=lambda item: item.created_at)

        for index, checkin in enumerate(ordered_checkins):
            remaining = len(ordered_checkins) - index
            if remaining <= target_active:
                continue

            if random.random() > 0.80:
                continue

            checkout_time = checkin.created_at + timedelta(hours=random.randint(18, 220))
            if checkout_time > timezone.now() - timedelta(hours=2):
                checkout_time = timezone.now() - timedelta(hours=random.randint(2, 36))

            checkout = Checkout.objects.create(checkin=checkin)
            Checkout.objects.filter(pk=checkout.pk).update(created_at=checkout_time)
            Checkin.objects.filter(pk=checkin.pk).update(active=False)

        # Ajuste final para nao ultrapassar muito a capacidade com dados de demo
        active_checkins = list(Checkin.objects.filter(active=True).order_by("created_at"))
        if len(active_checkins) > target_active:
            excess = len(active_checkins) - target_active
            for checkin in active_checkins[:excess]:
                if Checkout.objects.filter(checkin=checkin).exists():
                    continue
                checkout_time = timezone.now() - timedelta(hours=random.randint(4, 72))
                checkout = Checkout.objects.create(checkin=checkin)
                Checkout.objects.filter(pk=checkout.pk).update(created_at=checkout_time)
                Checkin.objects.filter(pk=checkin.pk).update(active=False)

    def _create_home_services(self, checkins, days_window):
        if not checkins:
            return

        now = timezone.now()
        service_records = []

        for checkin in checkins:
            base_records = random.randint(0, 2)
            if checkin.active:
                base_records += random.randint(1, 2)

            for _ in range(base_records):
                breakfast = random.random() < 0.60
                lunch = random.random() < 0.72
                snack = random.random() < 0.48
                dinner = random.random() < 0.69
                shower = random.random() < 0.41
                sleep = random.random() < 0.34

                if not any([breakfast, lunch, snack, dinner, shower, sleep]):
                    dinner = True

                service = HomeServices.objects.create(
                    person=checkin.person,
                    breakfast=breakfast,
                    lunch=lunch,
                    snack=snack,
                    dinner=dinner,
                    shower=shower,
                    sleep=sleep,
                )

                created_at = self._random_datetime_within_days(min(days_window, 30))
                if created_at > now:
                    created_at = now - timedelta(hours=1)

                HomeServices.objects.filter(pk=service.pk).update(
                    created_at=created_at,
                    updated_at=created_at,
                )
                service_records.append(service)

        return service_records

    @staticmethod
    def _random_datetime_within_days(days):
        now = timezone.now()
        start = now - timedelta(days=days)
        seconds_range = int((now - start).total_seconds())
        random_seconds = random.randint(0, max(seconds_range, 1))
        return start + timedelta(seconds=random_seconds)
