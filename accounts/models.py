from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):

    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    gender = models.CharField(choices=SEX_CHOICES, max_length=1)
    # edit it
    birthdate = models.DateField(null=True)
    email = models.EmailField(unique=True)
    confirmed = models.BooleanField(default=False)

    uuid = models.UUIDField(null=True, blank=True)

    def age(self):
        pass

    #REQUIRED_FILES = ['sex', 'birthday']
