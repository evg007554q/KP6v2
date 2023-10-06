from django.urls import path

from appmailsend.apps import AppmailsendConfig

from appmailsend.views import index, mailingsettingsListView, ClientCreateView, ClientUpdateView, \
    ClientDetailView, mailingsettingsCreateView, mailingsettingsUpdateView, mailingsettingsDetailView, ClientListView, \
    ClientDeleteVeiw, mailingsettingsDeleteVeiw, mailinglogListView, mailinglogDeleteVeiw, mailinglogDetailView, \
    new_app_send_mail_schedule

app_name = AppmailsendConfig.name
urlpatterns = [
    path('', index, name='index'),

    path('client/', ClientListView.as_view(), name='client'),
    path('client/create/', ClientCreateView.as_view(), name='Client_create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='Client_update'),
    path('info/<int:pk>/', ClientDetailView.as_view(), name='detail_Client'),
    path('delete/<int:pk>', ClientDeleteVeiw.as_view(), name='Client_delete'),

    path('mailingsettings/', mailingsettingsListView.as_view(), name='mailingsettings'),
    path('mailingsettings/create/', mailingsettingsCreateView.as_view(), name='mailingsettings_create'),
    path('mailingsettings/<int:pk>/update/', mailingsettingsUpdateView.as_view(), name='mailingsettings_update'),
    path('mailingsettings_info/<int:pk>/', mailingsettingsDetailView.as_view(), name='mailingsettings_detail'),
    path('mailingsettings_delete/<int:pk>', mailingsettingsDeleteVeiw.as_view(), name='mailingsettings_delete'),
    # path('mailingsettings/send_test/', send_test_mail, name='mailingsettings_send_test_mail'),

    path('mailinglog/', mailinglogListView.as_view(), name='mailinglog'),
    path('mailinglog_info/<int:pk>/', mailinglogDetailView.as_view(), name='mailinglog_detail'),
    path('mailinglog_delete/<int:pk>', mailinglogDeleteVeiw.as_view(), name='mailinglog_delete'),

    path('mailinglog/test_send_mail_schedule/', new_app_send_mail_schedule, name='new_app_send_mail_schedule'),
]
# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
