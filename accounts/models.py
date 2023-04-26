import datetime

from django.db import models
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    age = models.IntegerField()
    thumbnail = models.ImageField(null=True, blank=True)

    REQUIRED_FIELDS = ["first_name", "last_name", "email", "age"]



def get_all_logged_in_users():
    time = timezone.now() - datetime.timedelta(days=1)
    sessions = Session.objects.filter(expire_date__gte= time)
    uid_list = []

    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    return User.objects.filter(id__in=uid_list)
