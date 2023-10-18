from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from social.posts.models import Post


@receiver(pre_save, sender=Post)
def generate_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.content)
