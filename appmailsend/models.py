from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

from config import settings


class Client(models.Model):
    """ Клиенты получатели рассылок от пользователей"""
    name = models.CharField(max_length=100, verbose_name='Клиент')
    description = models.CharField(max_length=250, verbose_name='Описание клиента', null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name='e-mail ')

    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='дата создания', null=True, blank=True)
    last_modified_date = models.DateTimeField(auto_now_add=True, verbose_name='дата последнего изменения', null=True,
                                              blank=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Создатель')

    def __str__(self):
        return f'{self.name} '

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('name',)

class mailingsettings(models.Model):
    """ Настройка рассылки"""
    mailing_time = models.TimeField(verbose_name='время рассылки')
    start_of_mailing = models.DateTimeField(verbose_name='Дата начала рассылки')
    day = "day"
    week = "week"
    month = "month"
    Mailing_schedule_ch=[
        (day, "Ежедневно"),
        (week, "Еженедельно"),
        (month, "Ежемесячно"),
    ]
    Mailing_schedule = models.CharField(max_length=5, choices=Mailing_schedule_ch, default=day, verbose_name='График рассылки')

    completed = "completed"
    created = "created"
    launched = "launched"
    status_ch = [
        (completed, "завершена"),
        (created, "создана"),
        (launched, "запущена"),
    ]

    status = models.CharField(max_length=10, choices=status_ch, default=day,
                                    verbose_name='Статус рассылки')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Создатель')
    # client = models.ManyToManyField(Client, Q(owner_id= Client.owner))
    # client = models.ManyToManyField(Client,  limit_choices_to={'owner': models.F('owner')}, null=True,blank=True, verbose_name='Получатели')
    client = models.ManyToManyField(Client, )

    subject_email = models.CharField(max_length=250, null=True, blank=True, verbose_name="Тема письма")
    body_email = models.TextField(null=True, blank=True, verbose_name="Тело письма")

    def __str__(self):
        return f'Рассылка начиная с {self.start_of_mailing} - {self.Mailing_schedule} в {self.mailing_time}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('start_of_mailing',)

class MailingMessage(models.Model):
    """Сообщение для рассылки не удобно, не логично перенес в настройку рассылки"""
    subject_email = models.CharField(max_length=250, verbose_name="Тема письма")
    body_email = models.TextField(verbose_name="Тело письма")
    settings = models.OneToOneField(to='mailingsettings', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Создатель')

    def __str__(self):
        return f'{self.subject_email}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения для рассылки '
        ordering = ('subject_email',)


class MailingLog(models.Model):
    """ лог рассылки """
    time_mailing = models.DateTimeField(verbose_name='Дата рассылки')
    succes_mail = models.BooleanField(default=False, verbose_name='Успешная отправка')
    answer = models.TextField(null=True, blank=True, verbose_name="Ответ сервера")


    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, blank=True,  verbose_name='Получатель')
    owner = models.ForeignKey('mailingsettings', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Создатель')

    def __str__(self):
        return f'{self.time_mailing} - {self.answer} '

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ('time_mailing',)

