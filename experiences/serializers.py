from rest_framework.serializers import ModelSerializer
from .models import Perk, Experience


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class ExperienceDetailSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"
