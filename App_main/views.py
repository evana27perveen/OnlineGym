from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Min, Q
from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
from App_auth.forms import MemberUpdateForm
from App_auth.models import MemberModel, AdminModel, TrainerModel
from App_main.forms import WorkoutPlanModelForm, DietChartModelForm, BMIForm
from App_main.models import WorkoutPlanModel, DietChartModel, BMIModel, MessageModel


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_trainer(user):
    return user.groups.filter(name='TRAINER').exists()


def is_member(user):
    return user.groups.filter(name='MEMBER').exists()


def index(request):
    return render(request, 'App_main/index.html')


@login_required(login_url='App_auth:login')
@user_passes_test(is_member)
def member_dashboard(request):
    profile = MemberModel.objects.get(user=request.user)
    message = MessageModel.objects.filter(receiver=request.user, receiver_seen=False).count()
    content = {
        'profile': profile,
        'message': message
    }
    return render(request, 'App_main/member_dashboard.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_member)
def my_diet_chart(request):
    profile = MemberModel.objects.get(user=request.user)
    diet = DietChartModel.objects.filter(trainee=profile.id).order_by('-issued').first()
    content = {
        'diet': diet
    }
    return render(request, 'App_main/diet_chart.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_member)
def my_workout(request):
    profile = MemberModel.objects.get(user=request.user)
    plans = '$'
    try:
        plans = WorkoutPlanModel.objects.filter(trainee=profile).order_by('-created')
    except ObjectDoesNotExist:
        plans = '$'
    content = {
        'plans': plans
    }
    return render(request, 'App_main/my_workout.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_member)
def member_health(request):
    if request.method == 'POST':
        height = float(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        age = int(request.POST.get('age'))
        sex = request.POST.get('sex')

        bmi = weight / (height / 100 * height / 100)
        weight_status = ''
        if bmi < 18.5:
            weight_status = 'Underweight'
        elif bmi < 25:
            weight_status = 'Healthy'
        elif bmi < 30:
            weight_status = 'Overweight'
        else:
            weight_status = 'Obese'

        user = request.user
        bmi_model = BMIModel(person=user, height=height, weight=weight, age=age, sex=sex, bmi=bmi,
                             weight_status=weight_status)
        bmi_model.save()
        status = weight_status
    else:
        try:
            bmi_object = BMIModel.objects.filter(person=request.user).order_by('-created').first()
            status = bmi_object.weight_status
        except (BMIModel.DoesNotExist, AttributeError):
            status = 'Not Checked Yet'

    return render(request, 'App_main/member_health.html', {'status': status})


@login_required(login_url='App_auth:login')
@user_passes_test(is_member)
def my_trainer(request):
    profile = MemberModel.objects.get(user=request.user)
    trainer = TrainerModel.objects.get(id=profile.my_trainer.id)
    content = {
        'profile': profile,
        'trainer': trainer
    }
    return render(request, 'App_main/my_trainer.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_member)
def health_stat(request):
    profile = MemberModel.objects.get(user=request.user)
    bmi_data = BMIModel.objects.filter(person=request.user).order_by('-created')[:12][::-1]
    content = {
        'profile': profile,
        'bmi_data': bmi_data
    }
    return render(request, 'App_main/health_stat.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_member)
def member_inbox(request):
    profile = MemberModel.objects.get(user=request.user)
    trainer = TrainerModel.objects.get(id=profile.my_trainer.id)
    messages = MessageModel.objects.filter(sender=request.user) | MessageModel.objects.filter(receiver=request.user)
    messages = messages.order_by('created')
    unseen = MessageModel.objects.filter(receiver=request.user, receiver_seen=False)
    for i in unseen:
        i.receiver_seen = True
        i.save()
    if request.method == 'POST':
        msg = request.POST.get('msg')
        msg_model = MessageModel(sender=request.user, receiver=trainer.user, message=msg)
        msg_model.save()
    content = {
        'messages': messages,
        'trainer': trainer
    }
    return render(request, 'App_main/inbox.html', context=content)


# ------------------------------------------------member end-------------------------------------------
# ------------------------------------------------admin start-------------------------------------------

@login_required(login_url='App_auth:login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    profile = AdminModel.objects.get(user=request.user)
    members = MemberModel.objects.all()
    content = {
        'profile': profile,
        'members': members.count(),
    }
    return render(request, 'App_main/admin_dashboard.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_admin)
def assign_trainers(request):
    members = MemberModel.objects.filter(my_trainer=None)
    trainers = TrainerModel.objects.all()
    content = {
        'members': members,
        'trainers': trainers,
    }
    return render(request, 'App_main/assign_trainers.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_admin)
def assign_trainer(request, pk):
    trainer_id = request.POST.get('trainer')
    trainer = TrainerModel.objects.get(id=trainer_id)
    member = MemberModel.objects.get(id=pk)
    member.my_trainer = trainer
    member.save()
    return HttpResponseRedirect(reverse('App_main:assign-trainers'))


@login_required(login_url='App_auth:login')
@user_passes_test(is_admin)
def total_members(request):
    members = MemberModel.objects.all()
    content = {
        'members': members
    }
    return render(request, 'App_main/total_members.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_admin)
def admin_health_stat(request):
    members = MemberModel.objects.all()
    content = {
        'members': members
    }
    return render(request, 'App_main/admin_health_stat.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_admin)
def admin_health_each(request, pk):
    member = MemberModel.objects.get(user_id=pk)
    bmi_data = BMIModel.objects.filter(person_id=pk).order_by('-created')[:12][::-1]
    plans = '$'
    try:
        plans = WorkoutPlanModel.objects.filter(trainee=member).order_by('-created').first()
    except ObjectDoesNotExist:
        plans = '$'
    charts = '$'
    try:
        charts = DietChartModel.objects.filter(trainee=member).order_by('-issued').first()
    except ObjectDoesNotExist:
        charts = '$'
    content = {
        'member': member,
        'bmi_data': bmi_data,
        'chart': charts,
        'plan': plans
    }
    return render(request, 'App_main/admin_health_each.html', context=content)


# ------------------------------------------------admin end-------------------------------------------
# ------------------------------------------------trainer start---------------------------------------

@login_required(login_url='App_auth:login')
@user_passes_test(is_trainer)
def trainer_dashboard(request):
    profile = TrainerModel.objects.get(user=request.user)
    members = MemberModel.objects.filter(my_trainer=profile)
    message = MessageModel.objects.filter(receiver=request.user, receiver_seen=False).count()
    content = {
        'profile': profile,
        'members': members.count(),
        'message': message
    }
    return render(request, 'App_main/trainer_dashboard.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_trainer)
def my_trainees(request):
    profile = TrainerModel.objects.get(user=request.user)
    members = MemberModel.objects.filter(my_trainer=profile)
    content = {
        'profile': profile,
        'members': members,
    }
    return render(request, 'App_main/my_trainees.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_trainer)
def workout_plan(request, pk):
    profile = TrainerModel.objects.get(user=request.user)
    member = MemberModel.objects.get(id=pk)
    plans = '$'
    try:
        plans = WorkoutPlanModel.objects.filter(trainer=profile, trainee=member).order_by('-created')
    except ObjectDoesNotExist:
        plans = '$'
    form = WorkoutPlanModelForm()
    if request.method == 'POST':
        form = WorkoutPlanModelForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save(profile, member)
                return HttpResponseRedirect(reverse('App_main:my-trainees'))
    content = {
        'form': form,
        'plans': plans
    }
    return render(request, 'App_main/workoutplan.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_trainer)
def diet_chart(request, pk):
    profile = TrainerModel.objects.get(user=request.user)
    member = MemberModel.objects.get(id=pk)
    charts = '$'
    try:
        charts = DietChartModel.objects.filter(trainer=profile, trainee=member).order_by('-issued')
    except ObjectDoesNotExist:
        charts = '$'
    form = DietChartModelForm()
    if request.method == 'POST':
        form = DietChartModelForm(request.POST)
        if form.is_valid():
            diet = form.save(commit=False)
            diet.trainer = profile
            diet.trainee = member
            diet.save()
            return HttpResponseRedirect(reverse('App_main:my-trainees'))
    content = {
        'form': form,
        'charts': charts,
        'member': member
    }
    return render(request, 'App_main/dietchart.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_trainer)
def trainer_health(request):
    if request.method == 'POST':
        height = float(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        age = int(request.POST.get('age'))
        sex = request.POST.get('sex')

        bmi = weight / (height / 100 * height / 100)
        weight_status = ''
        if bmi < 18.5:
            weight_status = 'Underweight'
        elif bmi < 25:
            weight_status = 'Healthy'
        elif bmi < 30:
            weight_status = 'Overweight'
        else:
            weight_status = 'Obese'

        user = request.user
        bmi_model = BMIModel(person=user, height=height, weight=weight, age=age, sex=sex, bmi=bmi,
                             weight_status=weight_status)
        bmi_model.save()
        status = weight_status
    else:
        try:
            bmi_object = BMIModel.objects.filter(person=request.user).order_by('-created').first()
            status = bmi_object.weight_status
        except (BMIModel.DoesNotExist, AttributeError):
            status = 'Not Checked Yet'

    return render(request, 'App_main/trainer_health.html', {'status': status})


@login_required(login_url='App_auth:login')
@user_passes_test(is_trainer)
def health_stat_trainer(request):
    bmi_data = BMIModel.objects.filter(person=request.user).order_by('-created')[:12][::-1]
    content = {
        'bmi_data': bmi_data
    }
    return render(request, 'App_main/health_stat_trainer.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_trainer)
def trainer_targets(request):
    profile = TrainerModel.objects.get(user=request.user)
    members = MemberModel.objects.filter(my_trainer=profile)
    content = {
        'profile': profile,
        'members': members,
    }
    return render(request, 'App_main/trainer_targets.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_trainer)
def target_stat(request, pk):
    member = MemberModel.objects.get(user_id=pk)
    bmi_data = BMIModel.objects.filter(person_id=pk).order_by('-created')[:12][::-1]
    content = {
        'member': member,
        'bmi_data': bmi_data
    }
    return render(request, 'App_main/target_stat.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_trainer)
def trainer_chatbox(request):
    profile = TrainerModel.objects.get(user=request.user)
    unseen_messages = MessageModel.objects.filter(receiver=request.user, receiver_seen=False)
    unseen_message_count = unseen_messages.values('sender', 'sender__first_name', 'sender__last_name',
                                                  'sender__id').annotate(
        count=Count('sender')).order_by('-count')

    seen_messages = MessageModel.objects.filter(receiver=request.user, receiver_seen=True)
    seen_message_count = seen_messages.values('sender', 'sender__first_name', 'sender__last_name',
                                              'sender__id').annotate(
        count=Count('sender')).order_by('-count')

    content = {
        'seen_message_count': seen_message_count,
        'unseen_message_count': unseen_message_count,
        'profile': profile
    }
    return render(request, 'App_main/trainer_chatbox.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_trainer)
def trainer_inbox(request, pk):
    profile = TrainerModel.objects.get(user=request.user)
    a = MemberModel.objects.get(user_id=pk)
    if a == request.user:
        aa = a
        messages = MessageModel.objects.filter(sender=request.user, receiver=a.user) | MessageModel.objects.filter(
            receiver=request.user, sender=a.user)
        messages = messages.order_by('created')
    else:
        aa = a
        messages = MessageModel.objects.filter(sender=request.user, receiver=a.user) | MessageModel.objects.filter(
            receiver=request.user, sender=a.user)
        messages = messages.order_by('created')
    unseen = MessageModel.objects.filter(receiver=request.user, receiver_seen=False).order_by('created')
    for i in unseen:
        i.receiver_seen = True
        i.save()
    if request.method == 'POST':
        msg = request.POST.get('msg')
        msg_model = MessageModel(sender=request.user, receiver=aa.user, message=msg)
        msg_model.save()
    content = {
        'messages': messages,
        'trainer': profile
    }
    return render(request, 'App_main/trainer_inbox.html', context=content)


@login_required(login_url='App_auth:login')
@user_passes_test(is_trainer)
def trainer_diet_list(request):
    charts = DietChartModel.objects.filter(trainer__user=request.user)
    content = {
        'charts': charts,
    }
    return render(request, 'App_main/diet_list.html', context=content)

