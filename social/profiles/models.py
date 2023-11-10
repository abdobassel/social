from django.db import models
from django.utils.text import slugify
from phonenumber_field import modelfields

from social.utils.profile_photo_api import profile_photo_path


class Profile(models.Model):
    user = models.OneToOneField("users.User", related_name="userprofiles", on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    profile_photo = models.ImageField(upload_to=profile_photo_path, default="profile_default.png")
    bio = models.TextField(max_length=300, blank=True)
    country = models.CharField(max_length=30, default="", blank=True, null=True)
    city = models.CharField(max_length=30)
    phone_number = modelfields.PhoneNumberField(blank=True)  # country code, national_number
    timestamp = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(auto_now=False, null=True)
    # Followers
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)

    def follow(self, userprofiles):
        self.followers.add(userprofiles)

    def unfollow(self, userprofiles):
        self.followers.remove(userprofiles)

    def check_followers(self, userprofiles):
        return self.followers.filter(id=userprofiles.id).exists()

    def followers_count(self):
        return self.followers.count()

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)
