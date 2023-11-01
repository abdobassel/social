import random
import string

from django.core.management.base import BaseCommand

from social.posts.models import PostHashtag


class Command(BaseCommand):
    help = "Generate random hashtags"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of hashtags to create")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]

        for _ in range(count):
            name = "#" + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
            slug = name.lower().replace("#", "")
            is_active = random.choice([True, False])
            PostHashtag.objects.create(name=name, slug=slug, is_active=is_active)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} random hashtags"))
