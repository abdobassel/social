from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "social.posts"

    def ready(self):
        import social.posts.signals  # noqa
