from tkinter import CASCADE
from django.db import models
from django.conf import settings


class House(models.Model):

    """Model Definition for Houses"""

    name = models.CharField(max_length=140)
    price_per_night = models.PositiveBigIntegerField(
        verbose_name="Price", help_text="Positive Numvers Only"
    )
    description = models.TextField()
    address = models.CharField(max_length=140)
    pet_allowed = models.BooleanField(
        default=True,
        verbose_name="Pets Allowed?",
        help_text="Does this house allow pests?",
    )

    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
