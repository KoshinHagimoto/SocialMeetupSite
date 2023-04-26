from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm, MyPasswordChangeForm, MypasswordResetForm, MySetPasswordForm


User = get_user_model()


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)


class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'registration/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'


class PasswordReset(PasswordResetView):
    subject_template_name = 'registration/mail_templates/password_reset/subject.txt'
    email_template_name = 'registration/mail_templates/password_reset/message.txt'
    template_name = 'registration/password_reset.html'
    form_class = MypasswordResetForm
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = MySetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'registration/password_reset_confirmation.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'registration/password_reset_finish.html'