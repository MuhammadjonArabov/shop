from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from common.base import BaseModel
from common.manager import CustomUserManager


class Gender(models.IntegerChoices):
    MALE = 1, _('Male')
    FEMALE = 2, _('Female')


class Role(models.IntegerChoices):
    ADMIN = 1, 'ADMIN',
    CASHIER = 2, 'CASHIER',
    WAREHOUSE_WORKER = 3, 'WAREHOUSE_WORKER'


class User(AbstractUser, BaseModel):
    last_name = None
    first_name = None

    name = models.CharField(_("Name of User"), max_length=255)
    phone = models.CharField(_("Phone Number"), max_length=14, unique=True, null=True, blank=True)
    photo = models.ImageField(_("Photo of User"), upload_to="userImages", blank=True, null=True)
    role = models.IntegerField(choices=Role.choices, default=Role.ADMIN)
    gender = models.PositiveSmallIntegerField(choices=Gender.choices, default=Gender.MALE)

    objects = CustomUserManager()
    EMAIL_FIELD = None
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name
