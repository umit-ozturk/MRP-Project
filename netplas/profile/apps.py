from django.apps import AppConfig

class ProfileAppConfig(AppConfig):
    name = 'profile'

    def ready(self):
        import profile.signals