from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'apps.api'

    def ready(self):
        super().ready()
        # from django.utils.module_loading import autodiscover_modules
        # autodiscover_modules('xx')
