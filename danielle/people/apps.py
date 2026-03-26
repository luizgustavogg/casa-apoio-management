from django.apps import AppConfig


class PeopleConfig(AppConfig):
    name = "people"
    verbose_name = "Gestão de pessoas"

    def ready(self):
        import people.signals  # noqa: F401
