from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(DefaultUserManager):
    """Custom User Manager."""

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User, automatically fills 'username' as email
        """
        return super(UserManager, self).create_user(
            email=email, username=email, password=password, **extra_fields
        )


class User(AbstractUser):
    """Custom User Model."""

    email = models.EmailField(_("email address"), unique=True)
    objects = UserManager()
