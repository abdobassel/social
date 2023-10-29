from django.contrib.auth.models import AbstractUser as DjangoAbstractUser
from django.contrib.auth.models import PermissionsMixin as DjangoPermissionsMixin
from django.db import models

from .managers import UserManager
from ..profiles.models import Profile


class User(DjangoAbstractUser, DjangoPermissionsMixin):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        PREFER_NOT_TO_SAY = "X", "Prefer not to say"

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    slug = models.SlugField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.MALE, blank=True)
    joined_date = models.DateField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ["-joined_date"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
