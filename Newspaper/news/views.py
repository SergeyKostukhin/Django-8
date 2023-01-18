from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


@login_required
def become_an_author(request):
    user = request.user
    authors = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        authors.user_set.add(user)
    return redirect('news')


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostList(ListView):
    model = Post
    ordering = 'date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news1.html'
    context_object_name = 'news1'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.option = 'news'
        return super().form_valid(form)


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')


class ArtCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('<int:pk>/articles')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.option = 'post'
        return super().form_valid(form)


class ArtEdit(LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class ArtDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')
