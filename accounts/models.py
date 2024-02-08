from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

import datetime

# Create your models here.


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )
        return self._create_user(email, password, **extra_fields)
    

class User(AbstractUser):

    first_name = models.CharField(max_length=150, default="")
    last_name = models.CharField(max_length=150, default="")
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, default="", blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to="media/")

    google_login = models.BooleanField(default=False)
    google_picture = models.CharField(max_length=300, blank=True, null=True, default=None)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()
