from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):

    title = "Filter by words!"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            reviews


class GoodOrBadFilter(admin.SimpleListFilter):

    title = "Filter by good or bad words!"
    parameter_name = "goodOrBad"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good Reviews"),
            ("bad", "Bad Reviews"),
        ]

    def queryset(self, request, reviews):
        select = self.value()
        if select == "good":
            return reviews.filter(rating__gt=3)
        elif select == "bad":
            return reviews.filter(rating__lt=3)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        GoodOrBadFilter,
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
    )
