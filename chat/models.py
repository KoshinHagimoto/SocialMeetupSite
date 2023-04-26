from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class SingleOneToOneRoom(models.Model):
    room_name = models.CharField(max_length=100, blank=True, unique=True)
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_user', null=False)
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_user', null=False)

    def __str__(self):
        return f"{self.first_user.username}-{self.second_user.username}-room"

    class Meta:
        unique_together = ["first_user", "second_user"]


class Message(models.Model):
    room = models.ForeignKey(SingleOneToOneRoom, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_sender")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}"
