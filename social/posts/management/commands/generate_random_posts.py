import random
from io import BytesIO
from random import sample

from PIL import Image, ImageDraw
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from social.posts.models import Post, PostHashtag
from social.users.models import User


def generate_random_image(width=800, height=600):
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    rect_coords = ((0, 0), (width, height))
    draw.rectangle(rect_coords, fill=(red, green, blue))
    image_io = BytesIO()
    image.save(image_io, format="JPEG")
    image_file = File(image_io)
    image_file.name = "random_image.jpg"  # Set the file name
    return image_file


class Command(BaseCommand):
    help = "Generate sample posts"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, default=10, help="Number of posts to generate")

    def handle(self, *args, **options):
        count = options["count"]
        user_ids = User.objects.values_list("id", flat=True)  # Fetch all user IDs
        hashtags = list(PostHashtag.objects.all())  # Fetch all available hashtags

        fake = Faker()

        for _ in range(count):
            user_id = random.choice(user_ids)
            post = Post.objects.create(
                user_id=user_id,
                content=fake.text(max_nb_chars=500),  # Generate random text
                timestamp=fake.date_time_this_decade(tzinfo=timezone.utc),  # Generate random timestamp
                # Fill in other field values with random data as needed
            )

            # Randomly select a subset of hashtags from the available hashtags and associate them with the post
            selected_hashtags = sample(hashtags, random.randint(1, 5))  # Adjust the range as needed
            post.hashtags.add(*selected_hashtags)

            # Create and assign a random image to the post
            post_photo = generate_random_image()
            post.post_photo.save("random_image.jpg", post_photo, save=True)

            self.stdout.write(self.style.SUCCESS(f"Successfully created post with ID {post.id}"))
