from django import forms
from django.forms import TimeInput, DateInput

from appmailsend.models import Client, mailingsettings, MailingMessage, MailingLog


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Client
        exclude = 'owner',
        fields = '__all__'


class mailingsettingsForm(StyleFormMixin, forms.ModelForm):
    def __init__(self,   *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'start_of_mailing':
                field.widget = DateInput(attrs={'type': 'date-local'})
            elif field_name == 'mailing_time':
                field.widget = TimeInput(attrs={'type': 'time'})



        self.fields['client'].queryset = Client.objects.filter(owner=self.user)
        # widgets = {'mailing_time': TimeInput()}

    class Meta:
        model = mailingsettings
        exclude = ('owner',)
        fields = '__all__'



