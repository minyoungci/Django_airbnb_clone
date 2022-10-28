# Generated by Django 4.1.2 on 2022-10-28 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="House",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=140)),
                (
                    "price_per_night",
                    models.PositiveBigIntegerField(
                        help_text="Positive Numvers Only", verbose_name="Price"
                    ),
                ),
                ("description", models.TextField()),
                ("address", models.CharField(max_length=140)),
                (
                    "pet_allowed",
                    models.BooleanField(
                        default=True,
                        help_text="Does this house allow pests?",
                        verbose_name="Pets Allowed?",
                    ),
                ),
            ],
        ),
    ]
