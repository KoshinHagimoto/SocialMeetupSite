from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Tag', max_length=50)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description')
    tag = models.ManyToManyField(Tag, verbose_name='Tag', blank=True)
    thumbnail = models.ImageField(null=True, blank=True)
    dateAdded = models.DateTimeField("create", auto_now_add=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_user')
    member = models.ManyToManyField(User, verbose_name='member', related_name='group_participants')

    def __str__(self):
        return self.name

    def set_host(self, user=None):
        if user:
            self.host = user

    def is_host(self, user):
        return user is not None and self.host.pk == user.pk


class Event(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_host')
    member = models.ManyToManyField(User, verbose_name='member', related_name='event_participants')
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description')
    thumbnail = models.ImageField(null=True, blank=True)
    held_date = models.DateField("Date")
    address = models.CharField('Address', max_length=30)
    dateAdded = models.DateTimeField("create", auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.poster.username



