from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "social.users"

    def ready(self):
        import social.users.signals  # noqa
