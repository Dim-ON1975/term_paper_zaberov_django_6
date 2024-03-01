from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy, reverse


from blog.models import Post
from blog.services import sending_mail
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin


from datetime import datetime
from django.shortcuts import redirect
from django.http import Http404


class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = None
    login_url = reverse_lazy('clients:error403')

    def handle_no_permission(self):
        return redirect(self.get_login_url())


class DataMixin:
    paginate_by = 5


class PostListView(DataMixin, ListView):
    """ Список постов """
    model = Post

    def get_queryset(self, *args, **kwargs):
        """ Отображение только опубликованных постов (фильтрация по полю is_published """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class PostDetailView(DetailView):
    """ Пост """
    model = Post

    def get_object(self, queryset=None):
        """" Счётчик просмотров """
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        if self.object.view_count == 100:
            sending_mail(self.object.title, self.object.creator.email)
        return self.object


class PostCreateView(RedirectPermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """ Форма создания поста """
    model = Post
    permission_required = 'blog.add_post'
    fields = ('creator', 'title', 'body', 'img', 'published_at', 'is_published')
    success_url = reverse_lazy('blog:blog_view')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name='content_manager').exists() or self.request.user.is_superuser:
            return self.object
        if not self.request.user.is_staff:
            raise Http404
        return self.object

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Присваиваем текущего пользователя полю user нового продукта
        form.instance.user = user
        # Сохраняем экземпляр модели перед вызовом super().form_valid()
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        # Изменяем аргументы формы, добавляя пользователя в их начальные значения
        kwargs['initial'] = {'creator': self.request.user}
        return kwargs


class PostUpdateView(RedirectPermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """ Форма редактирования поста """
    model = Post
    permission_required = 'blog.change_post'
    fields = ('creator', 'title', 'body', 'img', 'published_at', 'is_published')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name='content_manager').exists() or self.request.user.is_superuser:
            return self.object
        if not self.request.user.is_staff:
            raise Http404
        return self.object

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Присваиваем текущего пользователя полю user нового продукта
        form.instance.user = user
        # Сохраняем экземпляр модели перед вызовом super().form_valid()
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        # Изменяем аргументы формы, добавляя пользователя в их начальные значения
        kwargs['initial'] = {'creator': self.request.user}
        return kwargs

    def get_success_url(self):
        """ Перенаправление на пост """
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Удаление поста """
    model = Post
    success_url = reverse_lazy('blog:blog_view')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.creator or self.request.user.is_superuser
