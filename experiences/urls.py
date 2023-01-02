from django.urls import path
from .views import Perks, PerkDetails

urlpatterns = [
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>", PerkDetails.as_view()),
]
