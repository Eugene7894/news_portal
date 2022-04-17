import pytz

# from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.utils import timezone
from django.shortcuts import redirect
from .models import Post, Category
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
        context['categories'] = Category.objects.all()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами
    #  ранее middleware в news/middlewares
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/news')


class CatPostsList(ListView):
    model = Post
    template_name = 'news/post_category.html'
    context_object_name = 'cat_news'
    ordering = ['-creationDate']
    paginate_by = 10

    def get_queryset(self, **kwargs):
        id_cat = self.kwargs.get('pk')
        current_cat = Category.objects.get(pk=id_cat)
        cust_queryset = current_cat.post_set.all()
        return cust_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_cat = self.kwargs.get('pk')
        current_cat = Category.objects.get(pk=id_cat)
        context['category_obj'] = current_cat
        context['is_not_subscribe'] = not current_cat.subscribers.filter(username=self.request.user.username).exists()
        return context


class PostDetails(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_post = self.kwargs.get('pk')
        current_cats = Category.objects.filter(post__pk=id_post)
        cat_bool_dict = {}
        for cat in current_cats:
            cat_bool_dict[cat] = not cat.subscribers.filter(username=self.request.user.username).exists()
        context['is_not_subscribe'] = cat_bool_dict
        return context

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)  # кэш очень похож на словарь, и метод get действует также.
        # Он забирает значение по ключу, если его нет, то забирает None.
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


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


