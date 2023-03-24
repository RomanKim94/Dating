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
        choices=SEX_CHOICES,
        max_length=1,
    )
    photo = models.ImageField(
        upload_to=get_file_path,
        blank=True,
        verbose_name='Profile picture',
    )
    age = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(150), MinValueValidator(18)],
    )
    email = models.EmailField(
        verbose_name='Email address'
    )
    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            PersonService.watermarking_photo(self.photo.path)


