import random
import secrets

from django.conf import settings
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserForm, UserForm_profile
from users.models import User

# Create your views here.
class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass

class RegisterView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            new_user.is_active = False

            key_user = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            new_user.key_user = key_user
            new_user.save()

            check_email_url = self.request.build_absolute_uri(reverse("users:check_email", kwargs={"key": new_user.key_user}))
            send_mail(
                subject='e-mail авторизация',
                message=f'Подтвердите регистрацию по ссылке {check_email_url}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]

            )
        return super().form_valid(form)




def check_email(request, key):
    user = get_object_or_404(User, key_user=key)
    user.is_active = True
    user.key_user = None
    user.save()
    return redirect('users:login')

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm_profile
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])


    send_mail(subject='Вы изменили пароль', message=f'Новый пароль {new_password}',
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[request.user.email]
              )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse_lazy('users:login'))