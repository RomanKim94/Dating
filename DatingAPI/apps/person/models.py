import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class Person(AbstractUser):

    def get_file_path(self, filename):
        username = self.username
        date = datetime.today().strftime('%Y.%m.%d')
        filename = uuid.uuid4[:10]+filename
        return f'photos/{username}/{date}/{filename}'

    SEX = {
        ('M', 'Male'),
        ('F', 'Female'),
    }

    sex = models.CharField(choices=SEX, max_length=1)
    photo = models.ImageField(upload_to=get_file_path)
    USERNAME_FIELD = 'username'



