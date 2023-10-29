from django.db import models

from social.utils.profile_photo_api import post_photo_path


class Post(models.Model):
    class Visibility(models.TextChoices):
        ONLY_ME = "ONY", "Only Me"
        EVERYONE = "EVN", "Everyone"

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    content = models.TextField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=600, blank=True, null=True)
    image = models.FileField(upload_to=post_photo_path, blank=True, null=True)
    likes = models.ManyToManyField("users.User", related_name="likes", blank=True)
    views = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    visibility = models.CharField(max_length=10, choices=Visibility.choices, default=Visibility.EVERYONE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)[:5]
