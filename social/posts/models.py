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
    reposted = models.ManyToManyField("users.User", related_name="retested_posts", blank=True)
    replies = models.ManyToManyField("Post", related_name="replied_to", blank=True)
    mentions = models.ManyToManyField("users.User", related_name="mentioned_in_post", blank=True)
    hashtags = models.ManyToManyField("PostHashtag", related_name="post_with_hashtag", blank=True)
    is_reposted = models.BooleanField(default=False)
    reposted_status = models.ForeignKey("Post", on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    visibility = models.CharField(max_length=10, choices=Visibility.choices, default=Visibility.EVERYONE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)[:5]


class PostHashtag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
