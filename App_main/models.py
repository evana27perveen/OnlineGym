from django.contrib.auth.models import User
from django.db import models
from App_auth.models import TrainerModel, MemberModel


# Create your models here.


class DietChartModel(models.Model):
    trainer = models.ForeignKey(TrainerModel, on_delete=models.CASCADE, related_name='chart_provider')
    trainee = models.ForeignKey(MemberModel, on_delete=models.CASCADE, related_name='chart_follower')
    sunday_breakfast = models.CharField(max_length=500)
    sunday_lunch = models.CharField(max_length=500)
    sunday_dinner = models.CharField(max_length=500)
    sunday_snacks = models.CharField(max_length=500)

    monday_breakfast = models.CharField(max_length=500)
    monday_lunch = models.CharField(max_length=500)
    monday_dinner = models.CharField(max_length=500)
    monday_snacks = models.CharField(max_length=500)

    tuesday_breakfast = models.CharField(max_length=500)
    tuesday_lunch = models.CharField(max_length=500)
    tuesday_dinner = models.CharField(max_length=500)
    tuesday_snacks = models.CharField(max_length=500)

    wednesday_breakfast = models.CharField(max_length=500)
    wednesday_lunch = models.CharField(max_length=500)
    wednesday_dinner = models.CharField(max_length=500)
    wednesday_snacks = models.CharField(max_length=500)

    thursday_breakfast = models.CharField(max_length=500)
    thursday_lunch = models.CharField(max_length=500)
    thursday_dinner = models.CharField(max_length=500)
    thursday_snacks = models.CharField(max_length=500)

    friday_breakfast = models.CharField(max_length=500)
    friday_lunch = models.CharField(max_length=500)
    friday_dinner = models.CharField(max_length=500)
    friday_snacks = models.CharField(max_length=500)

    saturday_breakfast = models.CharField(max_length=500)
    saturday_lunch = models.CharField(max_length=500)
    saturday_dinner = models.CharField(max_length=500)
    saturday_snacks = models.CharField(max_length=500)
    issued = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.issued} {self.trainer.user.first_name} {self.trainer.user.last_name}-{self.trainee.user.first_name} {self.trainee.user.last_name}"


class Workout(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class WorkoutPlanModel(models.Model):
    trainer = models.ForeignKey(TrainerModel, on_delete=models.CASCADE, related_name='plan_provider')
    trainee = models.ForeignKey(MemberModel, on_delete=models.CASCADE, related_name='plan_follower')
    sunday = models.ManyToManyField(Workout, related_name='sunday_plan')
    monday = models.ManyToManyField(Workout, related_name='monday_plan')
    tuesday = models.ManyToManyField(Workout, related_name='tuesday_plan')
    wednesday = models.ManyToManyField(Workout, related_name='wednesday_plan')
    thursday = models.ManyToManyField(Workout, related_name='thursday_plan')
    friday = models.ManyToManyField(Workout, related_name='friday_plan')
    saturday = models.ManyToManyField(Workout, related_name='saturday_plan')
    duration = models.PositiveIntegerField(default=0)
    created = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.created} {self.trainer.user.first_name} {self.trainer.user.last_name}-{self.trainee.user.first_name} {self.trainee.user.last_name}"


class BMIModel(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bmi_user')
    height = models.FloatField()
    weight = models.FloatField()
    age = models.IntegerField()
    sex = models.CharField(max_length=6)
    bmi = models.FloatField()
    weight_status = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name}'s BMI: {self.bmi}"


class MessageModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_user')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_user')
    receiver_seen = models.BooleanField(default=False)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.first_name}-{self.receiver.first_name}"
