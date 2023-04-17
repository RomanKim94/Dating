import os
from datetime import date
from math import radians, acos, cos, sin

from PIL import Image
from django.db.models import Func, F, ExpressionWrapper, DecimalField
from django.conf import settings
from decimal import Decimal

from django.db.models.functions import Coalesce


class PersonService:

    @staticmethod
    def get_distance(user, person):
        radius_km = 6367.4

        user_long = radians(user.longitude)
        user_lat = radians(user.latitude)
        person_long = radians(person.longitude)
        person_lat = radians(person.latitude)

        distance = radius_km * acos(
            cos(user_lat) * cos(person_lat) *
            cos(person_long - user_long) +
            sin(user_lat) * sin(person_lat)
        )
        return distance

    @staticmethod
    def add_distance_to_queryset(user, qs):
        radius_km = 6367.4
        user_lon_rad = Radians(user.longitude)
        user_lat_rad = Radians(user.latitude)
        qs = qs.annotate(
            distance=Coalesce(
                ExpressionWrapper(
                    radius_km * Acos(
                        Cos(user_lat_rad) * Cos(Radians(F('latitude'))) *
                        Cos(Radians(F('longitude')) - user_lon_rad) +
                        Sin(user_lat_rad) * Sin(Radians(F('latitude')))
                    ), output_field=DecimalField()
                ), Decimal(0)
            )
        )
        return qs

    @staticmethod
    def filter_by_distance(params, qs):
        max_distance = params.get('max_distance')
        min_distance = params.get('min_distance')
        if max_distance is not None:
            max_distance = Decimal(max_distance)
            qs = qs.filter(distance__lte=max_distance)
        if min_distance is not None:
            min_distance = Decimal(min_distance)
            qs = qs.filter(distance__gte=min_distance)
        return qs

    @staticmethod
    def filter_by_sex(params, qs):
        sex = params.get('sex')
        if sex is not None:
            sex = sex.lower()
            if sex in ['m', 'male', 'man', 'men']:
                sex = 'M'
            elif sex in ['f', 'female', 'woman', 'women']:
                sex = 'F'
            qs = qs.filter(sex=sex)
        return qs

    @staticmethod
    def filter_by_age(params, qs):
        max_age = params.get('max_age')
        min_age = params.get('min_age')
        today = date.today()
        if max_age is not None:
            earliest_birthday = date(today.year-int(max_age), today.month, today.day)
            qs = qs.filter(birthday__gte=earliest_birthday)
        if min_age is not None:
            latest_birthday = date(today.year - int(min_age), today.month, today.day)
            qs = qs.filter(birthday__lte=latest_birthday)
        return qs

    @staticmethod
    def queryset_filter(params, qs):
        for filter_function in [
            PersonService.filter_by_sex,
            PersonService.filter_by_age,
            PersonService.filter_by_distance,
        ]:
            qs = filter_function(params, qs)
        return qs

    @staticmethod
    def watermarking_photo(photo_path: str):
        with (
            Image.open(photo_path) as photo,
            Image.open(os.path.join(settings.BASE_DIR, 'apps/person/static/picture.jpg')) as watermark,
            Image.open(os.path.join(settings.BASE_DIR, 'apps/person/static/mask.jpg')) as mask,
        ):
            mask = mask.convert('L')
            watermark = watermark.convert('RGBA')
            photo_size_h = photo.size[1]
            watermark_size_h = watermark.size[1]
            photo.paste(watermark, (0, photo_size_h-watermark_size_h), mask=mask)
            photo.save(photo_path)


class Sin(Func):
    function = 'SIN'


class Cos(Func):
    function = 'COS'


class Acos(Func):
    function = 'ACOS'


class Radians(Func):
    function = 'RADIANS'
