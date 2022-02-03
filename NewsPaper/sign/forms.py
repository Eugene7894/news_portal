from django.forms import ModelForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django import forms


class ProfileForm(ModelForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email")


class BasicSignupForm(SignupForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "first_name",
                "placeholder": ("First name"),
                "autocomplete": "first_name",
                }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "last_name",
                "placeholder": ("Last name"),
                "autocomplete": "last_name",
                }
        )
    )

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
