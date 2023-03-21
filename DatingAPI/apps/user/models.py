from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    SEX = {
        ('M', 'Male'),
        ('F', 'Female'),
    }

    sex = models.CharField(choices=SEX, max_length=1)
    photo = models.ImageField(
        upload_to=lambda user, filename: 'photos/%(id)s/%Y/%m/%d/%(filename)s' % {'id': user.id, 'filename': filename}
    )
    # Yellow mark: may return an exception. Try this and override if exception is thrown
    USERNAME_FIELD = 'username'



