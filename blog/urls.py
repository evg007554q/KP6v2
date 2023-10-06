from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogListVeiw, BlogDetailVeiw, BlogUpdateView, BlogDeleteVeiw

app_name = BlogConfig.name

urlpatterns = [
    path('create/', BlogCreateView.as_view(), name='create'),
    path('', BlogListVeiw.as_view(), name='list'),
    path('view/<int:pk>', BlogDetailVeiw.as_view(), name='view'),
    path('edit/<int:pk>', BlogUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', BlogDeleteVeiw.as_view(), name='delete'),
]
  # + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
