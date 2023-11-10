# Generated by Django 4.2.6 on 2023-11-10 23:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="followers",
            field=models.ManyToManyField(
                blank=True, related_name="following", to="profiles.profile"
            ),
        ),
    ]
