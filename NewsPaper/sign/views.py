from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group, User
from news.models import Category
from .forms import ProfileForm


class UserDetails(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'sign/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'sign/profile_edit.html'
    form_class = ProfileForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return User.objects.get(pk=id)


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/')


@login_required
def subscribe_me(request, **kwargs):
    id_cat = kwargs.get('pk')
    user = request.user
    sub_cat = Category.objects.get(pk=id_cat)
    sub_user = User.objects.get(pk=user.pk)
    if sub_cat.subscribers.filter(id=user.pk):
        sub_cat.subscribers.remove(sub_user)
        return redirect(f'/news/category/{id_cat}')
    else:
        sub_cat.subscribers.add(sub_user)
        return redirect(f'/news/category/{id_cat}')
