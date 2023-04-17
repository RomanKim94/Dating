import uuid
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager
from .services import PersonService


class Person(AbstractUser):

    def get_file_path(self, filename):
        username = self.username
        date = datetime.today().strftime('%Y.%m.%d')
        filename = f'{str(uuid.uuid4())[:10]}{filename}'
        return f'photos/{username}/{date}/{filename}'

    SEX_CHOICES = {
        ('M', 'Male'),
        ('F', 'Female'),
    }

    sex = models.CharField(
        verbose_name='Sex of Person',
        choices=SEX_CHOICES,
        max_length=1,
    )
    photo = models.ImageField(
        verbose_name='Profile picture',
        upload_to=get_file_path,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name='Date of birth',
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Email address',
    )
    latitude = models.DecimalField(
        verbose_name='User latitude',
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        verbose_name='User longitude',
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            PersonService.watermarking_photo(self.photo.path)


