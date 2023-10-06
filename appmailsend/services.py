import smtplib
from datetime import datetime

from django.core.mail import send_mail

from appmailsend.models import MailingLog, mailingsettings
from config import settings


def app_send_mail(mailingsettings):
    """Разовая рассылка писем по настройке без расписания"""
    d1=datetime.now()

    for cl in mailingsettings.client.all():

        succes_mail = False
        try:

            res_answer = send_mail(mailingsettings.subject_email, message=f'{cl.name} {mailingsettings.body_email}',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[cl.email]
            )

            if res_answer:
                answer = ''
                succes_mail = True

        except smtplib.SMTPException as error:
            answer = str(error)



        MailingLog.objects.create(
            time_mailing = d1,
            succes_mail = succes_mail,
            answer = answer,
            client = cl,
            owner = mailingsettings.owner,
        )




def app_send_mail_schedule():
    """рассылка писем """
    # Текущая дата время
    d1 = datetime.now()
    for item_ms in mailingsettings.objects.filter(status='launched'):
        # Определим дату рассыки
        if item_ms.day:
            # ежедневно
            print(item_ms.Mailing_schedule)
        elif item_ms.week:
            # каждую неделю
            # номер дня старта
            # дата на этой неделю
            print('2')
            print(item_ms.Mailing_schedule)
        elif item_ms.month:
            # каждый месяц
            # номер дня старта
            # дата в этом месяце
            print(item_ms.Mailing_schedule)

    # Добавм время к дате рассылки

# send_mail(subject='Вы изменили пароль', message=f'Новый пароль {new_password}',
#           from_email=settings.EMAIL_HOST_USER,
#           recipient_list=[request.user.email]
#           )
