from django.urls import path
from . import views

app_name = 'App_main'

urlpatterns = [
    path('', views.index, name='index'),
    # admin
    path('member-dashboard', views.member_dashboard, name='member-dashboard'),
    path('admin-dashboard', views.admin_dashboard, name='admin-dashboard'),
    path('trainer-dashboard', views.trainer_dashboard, name='trainer-dashboard'),
    path('assign-trainers', views.assign_trainers, name='assign-trainers'),
    path('assign-trainer/<int:pk>/', views.assign_trainer, name='assign-trainer'),
    path('total-members', views.total_members, name='total-members'),
    path('admin-health-stat', views.admin_health_stat, name='admin-health-stat'),
    path('admin-health-each/<int:pk>/', views.admin_health_each, name='admin-health-each'),
    # trainer
    path('my-trainees', views.my_trainees, name='my-trainees'),
    path('workout-plan/<int:pk>/', views.workout_plan, name='workout-plan'),
    path('dietchart/<int:pk>/', views.diet_chart, name='dietchart'),
    path('trainer-health/', views.trainer_health, name='trainer-health'),
    path('health-stat-trainer/', views.health_stat_trainer, name='health-stat-trainer'),
    path('trainer-targets/', views.trainer_targets, name='trainer-targets'),
    path('target-stat/<int:pk>/', views.target_stat, name='target-stat'),
    path('trainer-inbox/<int:pk>/', views.trainer_inbox, name='trainer-inbox'),
    path('trainer-chatbox/', views.trainer_chatbox, name='trainer-chatbox'),
    path('trainer-diet-list/', views.trainer_diet_list, name='trainer-diet-list'),
    # member
    path('member-health/', views.member_health, name='member-health'),
    path('my-trainer/', views.my_trainer, name='my-trainer'),
    path('my-diet/', views.my_diet_chart, name='my-diet'),
    path('my-workout/', views.my_workout, name='my-workout'),
    path('health-stat/', views.health_stat, name='health-stat'),
    path('inbox/', views.member_inbox, name='inbox'),
]
