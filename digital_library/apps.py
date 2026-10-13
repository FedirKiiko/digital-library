from django.apps import AppConfig


class DigitalLibraryConfig(AppConfig):
    name = 'digital_library'

    def ready(self):
        import digital_library.signals
