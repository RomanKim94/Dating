import os

from PIL import Image


class PersonService:

    @staticmethod
    def watermarking_photo(path: str):
        with (
            Image.open(path) as photo,
            Image.open('apps/person/static/picture.jpg') as watermark,
            Image.open('apps/person/static/mask.jpg') as mask,
        ):
            mask = mask.convert('L')
            watermark = watermark.convert('RGBA')
            photo_size_h = photo.size[1]
            watermark_size_h = watermark.size[1]
            photo.paste(watermark, (0, photo_size_h-watermark_size_h), mask=mask)
            photo.save(path)


