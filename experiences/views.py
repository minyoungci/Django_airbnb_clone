from django.db import transaction
from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from categories.models import Category
from . import models
from . import serializers
from bookings.models import Booking
from bookings.serializers import (
    PublicBookingSerializer,
    CreateExperienceBookingSerializer,
)


class Perks(APIView):
    def get(self, request):
        all_perks = models.Perk.objects.all()
        serializer = serializers.PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(serializers.PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetails(APIView):
    def get_object(self, pk):
        try:
            return models.Perk.objects.get(pk=pk)
        except models.Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(
                serializers.PerkSerializer(updated_perk).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class Experiences(APIView):
    def get(self, request):
        experiences = models.Experience.objects.all()
        seiralizer = serializers.ExperienceSerializer(experiences, many=True)

        return Response(seiralizer.data)

    def post(self, request):
        serializer = serializers.ExperienceSerializer(data=request.data)

        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required")

            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("category is required")

            except Category.DoesNotExist:
                raise ParseError(detail="Category not found")

            try:
                with transaction.atomic():
                    experience = serializer.save(host=request.user, category=category)
                    perks = request.data.get("perks")

                    for perk_id in perks:
                        perk = models.Perk.objects.get(pk=perk_id)
                        experience.perks.add(perk)

                        return Response(
                            serializers.ExperienceSerializer(experience).data
                        )
            except Exception:
                raise ParseError("perk not found")

        else:
            return Response(serializer.errors)


class ExperienceDetails(APIView):
    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except models.Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        return Response(serializers.ExperienceDetailSerializer(experience).data)

    def put(self, request, pk):
        experience = self.get_object(pk)

        if experience != request.user:
            raise PermissionDenied

        serializer = serializers.ExperienceSerializer(
            experience, data=request.data, partial=True
        )

        if serializer.is_valid():
            category_pk = request.data.get("category")

            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise ParseError("The category kind should be Experience")
                except Category.DoesNotExist:
                    raise ParseError(detail="Category not found")

            try:
                with transaction.atomic():
                    if category_pk:
                        experience = serializer.save(category=category)
                    else:
                        experience = serializer.save()

                    perks = request.data.get("perks")

                    if perks:
                        experience.perks.clear()
                        for perk_pk in perks:
                            perk = models.Perk.objects.get(pk=perk_pk)
                            experience.perks.add(perk)

                    return Response(serializers.ExperienceSerializer(experience).data)
            except Exception:
                raise ParseError("Perk not found")

        else:
            return Response(serializers.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)

        if experience.host != request.user:
            raise PermissionDenied

        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except models.Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_object(pk)
        serializer = serializers.PerkSerializer(
            experience.perks.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class ExperienceBookings(APIView):
    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except models.Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))

        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gt=now,
        )[start:end]
        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(data=request.data)

        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookingDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_experience(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except models.Experience.DoesNotExist:
            raise NotFound

    def get_booking(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DeesNotExist:
            raise NotFound

    def get(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)

        return Response(PublicBookingSerializer(booking).data)

    def put(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)

        if booking.user.pk != request.user.pk:
            raise PermissionDenied

        serializer = CreateExperienceBookingSerializer(
            booking, data=request.data, partial=True
        )

        if serializer.is_valid():
            booking = serializer.save()
            serializer = PublicBookingSerializer(booking)

            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def delete(self, request, pk, booking_pk):

        booking = self.get_booking(booking_pk)

        if booking.user.pk != request.user.pk:
            raise PermissionDenied

        booking.delete()

        return Response(status=HTTP_204_NO_CONTENT)
