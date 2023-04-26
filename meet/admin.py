from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Tag, Group, Event, Comment

User = get_user_model()

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Group)
admin.site.register(Event)
admin.site.register(Comment)
