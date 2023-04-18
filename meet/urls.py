from django.urls import path
from . import views

app_name = 'meet'

urlpatterns = [
    path('meet/', views.MeetIndexView.as_view(), name='index'),
    path('meet/create/', views.MeetGroupCreateView.as_view(), name='group_create'),
    path('meet/detail/<int:pk>/', views.group_detail_view, name='group_detail'),
    path('meet/delete/<int:pk>/', views.MeetGroupDeleteView.as_view(), name='group_delete'),
    path('meet/update/<int:pk>/', views.MeetGroupUpdateView.as_view(), name='group_update'),
    path('meet/detail/<int:group_id>/create/', views.MeetEventCreateView.as_view(), name='event_create'),
    path('meet/delete/<int:group_id>/<int:pk>/', views.MeetEventDeleteView.as_view(), name='event_delete'),
    path('meet/update/<int:group_id>/<int:pk>/', views.MeetEventUpdateView.as_view(), name='event_update'),
    path('meet/detail/<int:group_id>/detail/<int:pk>/', views.event_detail_view, name='event_detail'),
    path('meet/detail/<int:group_id>/create/<int:pk>/', views.MeetCommentCreateView.as_view(), name='comment_create'),
]