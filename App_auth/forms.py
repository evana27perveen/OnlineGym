from django import forms
from .models import *
from django.contrib.auth import forms as auth_form


class AdminUserForm(auth_form.UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class AdminForm(forms.ModelForm):
    class Meta:
        model = AdminModel
        exclude = ['user', 'joining_date', 'status']


class TrainerUserForm(auth_form.UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class TrainerForm(forms.ModelForm):
    class Meta:
        model = TrainerModel
        exclude = ['user', 'joining_date', 'status']


class MemberUserForm(auth_form.UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class MemberForm(forms.ModelForm):
    class Meta:
        model = MemberModel
        exclude = ['user', 'joining_date', 'status']


class MemberUpdateForm(forms.ModelForm):
    my_trainer = forms.ModelChoiceField(queryset=TrainerModel.objects.all())

    class Meta:
        model = MemberModel
        fields = ['my_trainer']

