from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer()
    amenities = AmenitySerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Room
        fields = "__all__"


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )
