import smtplib
from calendar import calendar
from datetime import datetime, timedelta

from django.core.mail import send_mail

from appmailsend.models import MailingLog, mailingsettings
from config import settings


def app_send_mail(mailingsettings):
    """Разовая рассылка писем по настройке без расписания"""
    d1=datetime.now()

    for cl in mailingsettings.client.all():

        succes_mail = False
        try:

            res_answer = send_mail(subject=mailingsettings.subject_email,
                                   message=f'{cl.name} {mailingsettings.body_email}',
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
            owner = mailingsettings,
        )

def app_send_mail_cl(mailingsettings, cl):
    """отправка письма """
    d1=datetime.now()
    print(f'subject_email {mailingsettings.subject_email}')
    print(cl.name)
    print(mailingsettings.body_email)
    print(cl.email)

    succes_mail = False
    try:
        res_answer = send_mail(subject=mailingsettings.subject_email,
                               message=f'{cl.name} {mailingsettings.body_email}',
                               from_email=settings.EMAIL_HOST_USER,
                               recipient_list=[cl.email]
                               )

        if res_answer:
            answer = ''
            succes_mail = True

    except smtplib.SMTPException as error:
        answer = str(error)

    MailingLog.objects.create(
        time_mailing=d1,
        succes_mail=succes_mail,
        answer=answer,
        client=cl,
        owner=mailingsettings,
    )


def app_send_mail_schedule():
    """рассылка писем """

    for item_ms in mailingsettings.objects.filter(status='launched'):
        d_today=datetime.today().date()
        # счет от даты последней отправки проще но правильно сделать по расписанию
        # каждый вторник во сколько-то или каждый месяц в указанный день
        # Определим дату рассыки
        if item_ms.day == item_ms.Mailing_schedule:
            # ежедневно
            d_send=d_today

        elif item_ms.week == item_ms.Mailing_schedule:
            # каждую неделю
            # номер дня старта
            # дата на этой неделю
            d_send=d_today + timedelta(days= item_ms.start_of_mailing.date().weekday() - d_today.weekday() )
        elif item_ms.month:
            # каждый месяц
            # номер дня старта
            # дата в этом месяце
            day_send = item_ms.start_of_mailing.day

            # Последний день месяца
            last_day_mtd = calendar.monthrange(d_today.year,d_today.month)

            if  day_send > last_day_mtd[1]:
                d_send = datetime(d_today.year, d_today.month, last_day_mtd[1])
            else:
                d_send = datetime(d_today.year, d_today.month, day_send)

        print(d_send)
        print(item_ms.mailing_time)
        # Добавим время настроек к дате рассылки без времени
        dt_send=datetime(d_send.year, d_send.month, d_send.day, item_ms.mailing_time.hour, item_ms.mailing_time.minute, item_ms.mailing_time.second )
        print(dt_send)
        # Текущая дата время
        #
        d1 = datetime.now()
        # текущая дата больше даты когда дб рассылка
        if d1 > dt_send:
            for cl in item_ms.client.all():
                mail_log = MailingLog.objects.filter(client=cl, owner=item_ms)
                last_log = mail_log.order_by('-time_mailing').first()
                if last_log == None:
                    app_send_mail_cl(item_ms, cl)
                else:
                    last_log_date = last_log.time_mailing.replace(tzinfo=None)
                    if dt_send>last_log_date:
                        #дата когда дб рассылка больше последней
                        app_send_mail_cl(item_ms, cl)


