from django.db import models
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    category_name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name

class Account(AbstractUser):

    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    email = models.EmailField(unique=True)
    confirmed = models.BooleanField(default=False)
    
    # profile 
    gender = models.CharField(choices=SEX_CHOICES, max_length=1)
    birthdate = models.DateField(null=True)
    bio = models.TextField(null=True, blank=True)

    # for reset password and email confirmation 
    reset_password_token = models.UUIDField(null=True, blank=True)
    confirm_email_token = models.UUIDField(null=True, blank=True)

    # following and followers 
    following = models.ManyToManyField('Account', related_name='followers')

    # social accounts
    facebook = models.CharField(max_length=50, null=True, blank=True)
    instagram = models.CharField(max_length=50, null=True, blank=True)
    twitter = models.CharField(max_length=50, null=True, blank=True)

    # categories 
    category = models.ManyToManyField(Category, related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []