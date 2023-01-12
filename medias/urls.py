from django.urls import path
from .views import PhotoDetail

urlpatterns = [
    path(
        "photos/<int:pk>",
    )
]
