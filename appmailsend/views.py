from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from appmailsend.forms import ClientForm
from appmailsend.models import Client, MailingLog, mailingsettings

# filted(succes_mail=1),
def index(request):
     context = {
          'object_count': Client.objects.all().count(),
          'Log_count': MailingLog.objects.all().count(),
          'succes_mail_count': MailingLog.objects.filter(succes_mail=True).count(),
          'mailingsettings_count': mailingsettings.objects.all().count(),
          'title': 'Твоя рассылка'
     }
     return render(request, 'appmailsend/index.html',context)

def ClientList(request):
    context = {
        'object_list': Client.objects.all(),
        'title': 'Все клиенты'
    }
    return render(request, 'appmailsend/Client.html', context)

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    extra_context = {
        'title': 'Добавление клиента'
    }
    form_class = ClientForm
    success_url = reverse_lazy('catalog:client')
    # login_url = 'users:login'
    #
    # def form_valid(self, form):
    #     self.object = form.save()
    #     self.object.owner = self.request.user
    #     self.object.save()
    #
    #     return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    extra_context = {
        'title': 'Редактирование клиента'
    }
    form_class = ClientForm
    success_url = reverse_lazy('catalog:client')

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if not self.object.owner == self.request.user and not self.request.is_superuser:
    #         raise PermissionDenied
    #     return self.object
    #
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
    #
    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #
    #     context_data['version_set'] = get_version_list(self.object.pk)
    #     return context_data


class mailingsettingsListView(ListView):
    model = mailingsettings
    extra_context = {
        'title': 'Настройка рассылки'
    }