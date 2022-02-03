# from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post
from .filters import NewsFilter
from .forms import PostForm


class PostsList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    # queryset = Post.objects.order_by("-creationDate")
    ordering = ['-creationDate']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetails(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news_search'
    ordering = ['-creationDate']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news/add_post.html'
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'news/add_post.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'news/delete_post.html'
    queryset = Post.objects.all()
    success_url = '/news/'
