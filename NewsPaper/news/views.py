# from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import NewsFilter
from .forms import PostForm


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    # queryset = Post.objects.order_by("-creationDate")
    ordering = ['-creationDate']
    paginate_by = 10


class PostDetails(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news_search'
    ordering = ['-creationDate']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreateView(CreateView):
    template_name = 'add_post.html'
    form_class = PostForm


class PostUpdateView(UpdateView):
    template_name = 'add_post.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'delete_post.html'
    queryset = Post.objects.all()
    success_url = '/news/'
