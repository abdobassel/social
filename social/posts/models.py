from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Post(models.Model):
    class Visibility(models.TextChoices):
        ONLY_ME = "ONY", "Only Me"
        EVERYONE = "EVN", "Everyone"

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    content = models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=600, blank=True, null=True)
    image = models.FileField(upload_to="post", blank=True, null=True)
    likes = models.ManyToManyField("users.User", related_name="likes", blank=True)
    views = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    visibility = models.CharField(max_length=10, choices=Visibility.choices, default=Visibility.EVERYONE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        words = self.content.split()
        short_content = " ".join(words[:5])
        if len(words) > 5:
            short_content += " ..."
        return short_content

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.content)}"
        super().save(*args, **kwargs)


class Gallery(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="gallery", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(timezone.now())

    def __str__(self):
        return str(self.post)
