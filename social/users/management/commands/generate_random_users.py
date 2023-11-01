import random
import string

from django.core.management.base import BaseCommand

from social.users.models import User


# from users.models import User


class Command(BaseCommand):
    help = "Generate random users"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of users to create")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]

        for _ in range(count):
            first_name = "".join(random.choice(string.ascii_letters) for _ in range(8))
            last_name = "".join(random.choice(string.ascii_letters) for _ in range(8))
            email = f"{first_name}.{last_name}@example.com"
            password = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
            User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} random users"))
