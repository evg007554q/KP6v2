from django.contrib import admin

from appmailsend.models import Client, mailingsettings, MailingMessage, MailingLog


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'email',)

    # search_fields = ('name', 'description')

@admin.register(mailingsettings)
class mailingsettingsAdmin(admin.ModelAdmin):
    list_display = ('Mailing_schedule','mailing_time','status',)

@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('subject_email',)

@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('time_mailing','succes_mail','answer',)