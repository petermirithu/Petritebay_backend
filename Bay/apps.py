from django.apps import AppConfig


class BayConfig(AppConfig):
    name = 'Bay'

    def ready(self):
        import Bay.signal
