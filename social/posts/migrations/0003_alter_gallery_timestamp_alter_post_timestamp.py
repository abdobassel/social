# Generated by Django 4.2.6 on 2023-10-17 07:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gallery",
            name="timestamp",
            field=models.DateTimeField(
                verbose_name=datetime.datetime(
                    2023, 10, 17, 7, 6, 13, 285413, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="timestamp",
            field=models.DateTimeField(
                verbose_name=datetime.datetime(
                    2023, 10, 17, 7, 6, 13, 284231, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
