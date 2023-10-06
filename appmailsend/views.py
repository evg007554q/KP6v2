from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from appmailsend.forms import ClientForm, mailingsettingsForm
from appmailsend.models import Client, MailingLog, mailingsettings
from appmailsend.services import app_send_mail, app_send_mail_schedule


def index(request):

    if request.user.is_authenticated:
        context = {

            'object_count': Client.objects.filter(owner=request.user).count(),
            'Log_count': MailingLog.objects.filter(owner=request.user).count(),
            'succes_mail_count': MailingLog.objects.filter(owner=request.user, succes_mail=True).count(),
            'mailingsettings_count': mailingsettings.objects.filter(owner=request.user).count(),
            'title': f'Рассылка пользователя - {request.user}'
        }
    else:
        context = {

            'object_count': 0,
            'Log_count': 0,
            'succes_mail_count': 0,
            'mailingsettings_count': 0,
            'title': f'Авторизуйтесь для работы с сервисом'
        }
    return render(request, 'appmailsend/index.html', context)



class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'клиенты'
    }
    template_name = 'client_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджер') or user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(owner=user.pk)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    extra_context = {
        'title': 'Добавление клиента'
    }
    form_class = ClientForm
    success_url = reverse_lazy('appmailsend:client')
    login_url = 'users:login'

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    extra_context = {
        'title': 'Редактирование клиента'
    }
    form_class = ClientForm
    success_url = reverse_lazy('appmailsend:client')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.object.owner == self.request.user and not self.request.is_superuser:
            raise PermissionDenied
        return self.object

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super().get_context_data(*args, **kwargs)
    #     VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
    #     if self.request.method == 'POST':
    #         context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
    #     else:
    #         context_data['formset'] = VersionFormset(instance=self.object)
    #
    #     # context_data['formset'] = formset
    #     return context_data
    #
    # def form_valid(self, form):
    #     # context_data =
    #     formset = self.get_context_data()['formset']
    #     self.object = form.save()
    #
    #     if formset.is_valid():
    #         formset.instance = self.object
    #         formset.save()
    #
    #     return super().form_valid(form)


class ClientDetailView(DetailView):
    model = Client
    extra_context = {
        'title': 'Информация по клиенту '
    }
    form_class = ClientForm
    success_url = reverse_lazy('appmailsend:client')

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #
    #     context_data['version_set'] = get_version_list(self.object.pk)
    #     return context_data

class ClientDeleteVeiw(DeleteView):
    model = Client
    extra_context = {
        'title': 'Delete Client'
    }
    success_url = reverse_lazy('appmailsend:client')

class mailingsettingsListView(LoginRequiredMixin, ListView):
    model = mailingsettings
    extra_context = {
        'title': 'Настройки рассылок'
    }
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджер') or user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(owner=user.pk)
        return queryset

class mailingsettingsCreateView(LoginRequiredMixin, CreateView):
    model = mailingsettings
    extra_context = {
        'title': 'Добавление рассылки'
    }
    form_class = mailingsettingsForm
    success_url = reverse_lazy('appmailsend:mailingsettings')
    login_url = 'users:login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class mailingsettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = mailingsettings
    extra_context = {
        'title': 'Редактирование рассылки'
    }
    form_class = mailingsettingsForm
    success_url = reverse_lazy('appmailsend:mailingsettings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.object.owner == self.request.user and not self.request.is_superuser:
            raise PermissionDenied
        return self.object

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class mailingsettingsDetailView(DetailView):
    model = mailingsettings
    extra_context = {
        'title': 'Информация по рассылке '
    }
    form_class = mailingsettingsForm
    success_url = reverse_lazy('appmailsend:mailingsettings')
    app_send_mail_schedule()

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #
    #
    # return context_data

class mailingsettingsDeleteVeiw(DeleteView):
    model = mailingsettings
    extra_context = {
        'title': 'Delete settings mailing'
    }
    success_url = reverse_lazy('appmailsend:mailingsettings')


class mailinglogListView(LoginRequiredMixin, ListView):
    model = MailingLog
    extra_context = {
        'title': 'Логи рассылок'
    }
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджер') or user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(owner=user.pk)
        return queryset


class mailinglogDetailView(DetailView):
    model = MailingLog
    extra_context = {
        'title': 'Детали рассылки'
    }
    form_class = mailingsettingsForm
    success_url = reverse_lazy('appmailsend:MailingLog')




class mailinglogDeleteVeiw(DeleteView):
    model = MailingLog
    extra_context = {
        'title': 'Delete MailingLog'
    }
    success_url = reverse_lazy('appmailsend:MailingLog')
