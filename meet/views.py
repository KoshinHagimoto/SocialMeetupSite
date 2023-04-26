from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import get_all_logged_in_users
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils import timezone

from .models import Tag, Group, Event, Comment
from .forms import GroupForm, EventForm, CommentForm
from .tasks import send_notification


class MeetIndexView(ListView):
    model = Group
    template_name = "meet/index.html"
    context_object_name = "group_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logged_in_users'] = get_all_logged_in_users()
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        q = self.request.GET.get('q') if self.request.GET.get('q') is not None else ''
        if q == 'mygroup':
            queryset = queryset.filter(Q(member=self.request.user) | Q(host=self.request.user)).distinct()
        elif q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(tag__name__icontains=q)).distinct()
        return queryset.order_by('-dateAdded')


class MeetGroupCreateView(LoginRequiredMixin, CreateView):
    template_name = 'meet/group_create.html'
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('meet:index')

    def form_valid(self, form):
        form.instance.host = self.request.user
        group = form.save(commit=False)
        tag_list = form.cleaned_data.get('tag')
        group.save()
        if tag_list:
            for tag in tag_list:
                group.tag.add(Tag.objects.get_or_create(name=tag)[0])
        form.save_m2m()
        send_notification(group, 'Created Group')
        return super().form_valid(form)


class MeetEventCreateView(LoginRequiredMixin, CreateView):
    template_name = 'meet/event_create.html'
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.host = self.request.user
        group = get_object_or_404(Group, pk=self.kwargs['group_id'])
        event = form.save(commit=False)
        event.group = group
        event.save()
        send_notification(event, 'event')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('meet:group_detail', kwargs={"pk": self.object.group.id})


class MeetGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'meet/group_delete.html'
    success_url = reverse_lazy('meet:index')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.host != self.request.user:
            raise PermissionDenied

        return obj


class MeetEventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'meet/event_delete.html'
    success_url = reverse_lazy('meet:index')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.host != self.request.user:
            raise PermissionDenied
        return obj


class MeetGroupUpdateView(UpdateView):
    model = Group
    fields = ['name', 'description', 'tag', 'thumbnail']
    template_name = 'meet/group_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.host != self.request.user:
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        group = form.save(commit=False)
        group.save()
        send_notification(group, 'Updated Group')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('meet:group_detail', kwargs={'pk': self.object.id})


class MeetEventUpdateView(UpdateView):
    model = Event
    fields = ['name', 'description', 'thumbnail', 'held_date', 'address']
    template_name = 'meet/event_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.host != self.request.user:
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        event = form.save(commit=False)
        event.save()
        send_notification(event, 'Updated Group')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('meet:event_detail', kwargs={'group_id': self.object.group.id, 'pk':self.object.id})


class MeetCommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.poster = self.request.user
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.event = event
        comment.save()
        return redirect('meet:event_detail', group_id=self.kwargs['group_id'], pk=self.kwargs['pk'])


def group_detail_view(request, **kwargs):
    group = Group.objects.get(pk__iexact=kwargs['pk'])
    template_name = 'meet/group_detail.html'

    context = dict()
    context["group"] = group
    context['previous_events'] = Event.objects.filter(group__id=kwargs['pk']).filter(
        held_date__lte=timezone.now()).order_by('held_date')
    context['upcoming_events'] = Event.objects.filter(group__id=kwargs['pk']).filter(
        held_date__gte=timezone.now()).order_by('held_date')

    if request.method == 'POST':
        if Group.objects.filter(id=kwargs['pk']).filter(member__exact=request.user):
            group.member.remove(request.user)
            send_notification(group, 'member removed')
        else:
            group.member.add(request.user)
            send_notification(group, 'member added')
    return render(request, template_name, context)


def event_detail_view(request, **kwargs):
    event = Event.objects.get(pk__iexact=kwargs['pk'])
    template_name = 'meet/event_detail.html'

    context = dict()
    context['event'] = event
    context['comment_list'] = Comment.objects.filter(event__id=kwargs['pk']).order_by('created_at')
    context['comment_form'] = CommentForm

    if request.method == 'POST':
        if Event.objects.filter(id=kwargs['pk']).filter(member__exact=request.user):
            event.member.remove(request.user)
            send_notification(event, 'member removed')
        else:
            event.member.add(request.user)
            send_notification(event, 'member added')
    return render(request, template_name, context)

