from django.urls import path
from .views import UserDetails, UserUpdateView, upgrade_me, subscribe_me

urlpatterns = [
    path('<int:pk>/profile/', UserDetails.as_view(), name='profile_details'),
    path('<int:pk>/profile/edit', UserUpdateView.as_view(), name='profile_edit'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('cat_subscription/<int:pk>', subscribe_me, name='cat_subscription'),
]