from django.urls import path
from django.views.decorators.cache import cache_page
from .views import PostsList, PostDetails, PostSearch, PostUpdateView, PostCreateView, PostDeleteView, CatPostsList


urlpatterns = [
    path('', cache_page(60*5)(PostsList.as_view()), name='news_list'),
    path('<int:pk>', PostDetails.as_view(), name='post'),
    path('search', PostSearch.as_view(), name='search'),
    path('add', PostCreateView.as_view(), name='post_add'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('category/<int:pk>', cache_page(60*5)(CatPostsList.as_view()), name='cat_news_list'),
]
