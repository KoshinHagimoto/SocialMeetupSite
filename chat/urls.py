from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('<int:pk>/', views.ChatView.as_view(), name='chat'),
]