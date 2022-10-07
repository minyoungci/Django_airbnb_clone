from django.contrib import admin
from .models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    fields = (
        "name",
        "address",
        ("price_per_night", "pets_allowed"),
    )

    list_display = ["name", "price_per_night", "address", "pet_allowed"]
    list_filter = ["price_per_night", "pet_allowed"]
    search_fields = [
        "address",
    ]
    list_display_links = ("name", "address")
    list_editable = ("pet_allowed",)


# Register your models here.
