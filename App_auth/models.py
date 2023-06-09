from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import *

# Create your models here.

gender_choice = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Third Gender", "Third Gender"),
)

phone_regex = RegexValidator(regex=r"^\+?(88)01[3-9][0-9]{8}$", message=_('Must add 880'))


class AdminModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_user')
    phone_number = models.CharField(validators=[phone_regex], verbose_name=_("Admin_phone"), max_length=14)
    address = models.CharField(max_length=150)
    gender = models.CharField(choices=gender_choice, max_length=15)
    profile_picture = models.ImageField(upload_to='admin_picture')
    joining_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Admin - {self.user.first_name} {self.user.last_name}"


class TrainerModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainer_user')
    phone_number = models.CharField(validators=[phone_regex], verbose_name=_("Trainer_phone"), max_length=14)
    address = models.CharField(max_length=150)
    gender = models.CharField(choices=gender_choice, max_length=15)
    profile_picture = models.ImageField(upload_to='trainer_picture')
    joining_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Trainer - {self.user.first_name} {self.user.last_name}"


class MemberModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member_user')
    phone_number = models.CharField(validators=[phone_regex], verbose_name=_("Member_phone"), max_length=14)
    address = models.CharField(max_length=150)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(choices=gender_choice, max_length=15)
    profile_picture = models.ImageField(upload_to='member_picture')
    joining_date = models.DateField(auto_now_add=True)
    my_trainer = models.ForeignKey(TrainerModel, on_delete=models.CASCADE, related_name='personal_trainer', blank=True,
                                   null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Member - {self.user.first_name} {self.user.last_name}"
