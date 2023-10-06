# Generated by Django 4.2.4 on 2023-10-04 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Содержание')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, null=True, verbose_name='дата публикации')),
                ('image', models.ImageField(blank=True, null=True, upload_to='image_Blog', verbose_name='изображение')),
                ('Published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('number_of_views', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('slug', models.CharField(blank=True, max_length=50, null=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
                'ordering': ('title',),
            },
        ),
    ]