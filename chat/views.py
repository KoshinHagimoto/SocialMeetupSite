from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.views.generic import DetailView, CreateView


from .models import SingleOneToOneRoom


class RoomCreateForm(ModelForm):
    class Meta:
        model = SingleOneToOneRoom
        fields = []

class ChatView(LoginRequiredMixin, DetailView):
    queryset = SingleOneToOneRoom.objects.prefetch_related('messages')
    template_name = 'chat/chat.html'