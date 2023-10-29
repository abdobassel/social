from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from social.profiles.models import Profile
from .models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a user profile when a new user is created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a user profile when a new user is created.
    """
    instance.profile.save()


@receiver(pre_save, sender=User)
def update_username(sender, instance, **kwargs):
    """
    Signal handler to generate and add counter to make the username unique
    """
    if not instance.username:
        username = f"{instance.first_name.lower()}{instance.last_name.lower()}"
        counter = 1
        while User.objects.filter(username=username):
            username = f"{instance.first_name.lower()}{instance.last_name.lower()}{counter}"
            counter += 1
        instance.username = username


@receiver(pre_save, sender=User)
def update_slug(sender, instance, **kwargs):
    """
    Signal handler to slugify a username and add-count number
    """
    if not instance.slug:
        base_slug = slugify(f"{instance.first_name}-{instance.last_name}")
        slug = base_slug
        count = 1
        while User.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1
        instance.slug = slug
