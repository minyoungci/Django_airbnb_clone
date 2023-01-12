from django.urls import path
from .views import PhotoDetaul

urlpatterns = [
    path(
        "photos/<int:pk>",
    )
]
