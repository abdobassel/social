from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from social.posts.models import Post
from social.users.models import User


class Command(BaseCommand):
    help = "Generate sample posts"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, default=10, help="Number of posts to generate")

    def handle(self, *args, **options):
        count = options["count"]
        user_ids = User.objects.values_list("id", flat=True)  # Fetch all user IDs

        fake = Faker()

        for _ in range(count):
            post = Post.objects.create(
                user_id=user_ids,
                content=fake.text(max_nb_chars=500),  # Generate random text
                timestamp=fake.date_time_this_decade(tzinfo=timezone.utc),  # Generate random timestamp
                # Fill in other field values with random data as needed
            )

            # Add likes, reposts, mentions, hashtags, or other related data as necessary
            # Example: post.likes.add(user1, user2)
            # Example: post.mentions.add(mentioned_user1, mentioned_user2)
            # Example: post.hashtags.add(hashtag1, hashtag2)

            self.stdout.write(self.style.SUCCESS(f"Successfully created post with ID {post.id}"))
