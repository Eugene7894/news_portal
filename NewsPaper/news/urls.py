from django.urls import path
from .views import PostsList, PostDetails, PostSearch, PostUpdateView, PostCreateView, PostDeleteView

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetails.as_view(), name='post'),
    path('search', PostSearch.as_view()),
    path('add', PostCreateView.as_view(), name='post_add'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
]
