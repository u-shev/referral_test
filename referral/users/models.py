from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from secrets import token_urlsafe
from .managers import UserManager


class User(AbstractUser):
    objects = UserManager()

    username = None
    email = None
    phone_number = PhoneNumberField(unique=True)
    referral_code = models.CharField(default=token_urlsafe(4),
                                   max_length=6, unique=True)
    invite_code = models.CharField(max_length=6, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone_number)