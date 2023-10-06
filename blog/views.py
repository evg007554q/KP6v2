from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title','description','image')
    extra_context = {
        'title': 'Новая запись в блоге'
    }
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title','description','image')
    extra_context = {
        'title': 'Update блог'
    }
    # success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])

class BlogListVeiw(ListView):
    model = Blog
    extra_context = {
        'title': 'Опубликованные записи в блоге'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(Published=True)
        return queryset
class BlogDetailVeiw(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        self.object.save()
        return self.object

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)

        category_item = Blog.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f'Blog {category_item.title }'

        return context_data

class BlogDeleteVeiw(DeleteView):
    model = Blog
    extra_context = {
        'title': 'Delete блог'
    }
    success_url = reverse_lazy('blog:list')