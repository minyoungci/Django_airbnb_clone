# Generated by Django 4.1.1 on 2022-11-07 11:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.PositiveIntegerField(
                validators=[django.core.validators.MaxValueValidator(5)]
            ),
        ),
    ]
