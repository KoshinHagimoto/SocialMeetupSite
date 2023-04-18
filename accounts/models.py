from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    age = models.IntegerField()
    thumbnail = models.ImageField(null=True, blank=True)

    REQUIRED_FIELDS = ["first_name", "last_name",  "email", "age"]
