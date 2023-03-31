import os

from PIL import Image
from django.db.models import Func, F, ExpressionWrapper, DecimalField
from django.conf import settings
from decimal import Decimal

from django.db.models.functions import Coalesce


class PersonService:

    @staticmethod
    def add_distance(user, qs):
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
