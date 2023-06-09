from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import *
from .forms import *


# Create your views here.


def admin_signup(request):
    form1 = AdminUserForm()
    form2 = AdminForm()
    if request.method == 'POST':
        form1 = AdminUserForm(data=request.POST)
        form2 = AdminForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            my_form1 = form1.save()
            my_form2 = form2.save(commit=False)
            my_form2.user = my_form1
            my_form2.save()
            admin_grp = Group.objects.get_or_create(name='ADMIN')
            admin_grp[0].user_set.add(my_form1)
            return HttpResponseRedirect(reverse('App_main:admin-dashboard'))
    return render(request, 'App_auth/admin_signup.html', context={'form1': form1, 'form2': form2})


def trainer_signup(request):
    form1 = TrainerUserForm()
    form2 = TrainerForm()
    if request.method == 'POST':
        form1 = TrainerUserForm(data=request.POST)
        form2 = TrainerForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            my_form1 = form1.save()
            my_form2 = form2.save(commit=False)
            my_form2.user = my_form1
            my_form2.save()
            trainer_grp = Group.objects.get_or_create(name='TRAINER')
            trainer_grp[0].user_set.add(my_form1)
            return HttpResponseRedirect(reverse('App_main:trainer-dashboard'))
    return render(request, 'App_auth/trainer_signup.html', context={'form1': form1, 'form2': form2})


def member_signup(request):
    form1 = MemberUserForm()
    form2 = MemberForm()
    if request.method == 'POST':
        form1 = MemberUserForm(data=request.POST)
        form2 = MemberForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            my_form1 = form1.save()
            my_form2 = form2.save(commit=False)
            my_form2.user = my_form1
            my_form2.save()
            member_grp = Group.objects.get_or_create(name='MEMBER')
            member_grp[0].user_set.add(my_form1)
            return HttpResponseRedirect(reverse('App_main:member-dashboard'))
    return render(request, 'App_auth/member_signup.html', context={'form1': form1, 'form2': form2})


def login_system(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.groups.filter(name__in=['ADMIN']).exists():
                return HttpResponseRedirect(reverse('App_main:admin-dashboard'))
            elif request.user.groups.filter(name__in=['TRAINER']).exists():
                return HttpResponseRedirect(reverse('App_main:trainer-dashboard'))
            elif request.user.groups.filter(name__in=['MEMBER']).exists():
                return HttpResponseRedirect(reverse('App_main:member-dashboard'))
            else:
                return HttpResponseRedirect(reverse('App_auth:login'))
    return render(request, 'App_auth/login.html')


def logout_system(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_main:index'))
