from django.contrib.auth.models import AbstractUser as DjangoAbstractUser
from django.contrib.auth.models import PermissionsMixin as DjangoPermissionsMixin
from django.db import models

from .managers import UserManager


class User(DjangoAbstractUser, DjangoPermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Extract the username from the email and set it
        if not self.username:
            self.username = self.email.split("@")[0]
        super().save(*args, **kwargs)
