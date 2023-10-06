from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=150,verbose_name='Заголовок')
    description = models.TextField(verbose_name='Содержание')
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации', null=True, blank=True)
    image = models.ImageField(upload_to='image_Blog', verbose_name='изображение', null=True, blank=True)

    Published = models.BooleanField(default=True, verbose_name='Опубликовано')
    number_of_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    slug = models.CharField(max_length=50, verbose_name='slug', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('title',)