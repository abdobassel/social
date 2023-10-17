from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField
from phonenumber_field import modelfields

from .profile_photo_api import profile_photo_path


class Profile(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    profile_photo = models.ImageField(upload_to=profile_photo_path, default="profile_default.png")
    bio = models.TextField(max_length=300, blank=True)
    country = CountryField(default="", blank=True, null=True)
    city = models.CharField(max_length=30)
    phone_number = modelfields.PhoneNumberField(blank=True)  # country code, national_number
    timestamp = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(auto_now=False, blank=True)

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("profiles:profile-detail", kwargs={"pk": self.pk})
