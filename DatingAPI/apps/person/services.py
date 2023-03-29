from PIL import Image
from django.db.models import Func


class PersonService:

    @staticmethod
    def watermarking_photo(path: str):
        with (
            Image.open(path) as photo,
            Image.open('/home/TestingDatingAPI/Dating/DatingAPI/apps/person/static/picture.jpg') as watermark,
            Image.open('/home/TestingDatingAPI/Dating/DatingAPI/apps/person/static/picture.jpg') as mask,
        ):
            mask = mask.convert('L')
            watermark = watermark.convert('RGBA')
            photo_size_h = photo.size[1]
            watermark_size_h = watermark.size[1]
            photo.paste(watermark, (0, photo_size_h-watermark_size_h), mask=mask)
            photo.save(path)


class Sin(Func):
    function = 'SIN'


class Cos(Func):
    function = 'COS'


class Acos(Func):
    function = 'ACOS'


class Radians(Func):
    function = 'RADIANS'
