from django.urls import path
from . import views


app_name = 'App_auth'

urlpatterns = [
    path('admin-signup/', views.admin_signup, name='admin-signup'),
    path('trainer-signup/', views.trainer_signup, name='trainer-signup'),
    path('member-signup/', views.member_signup, name='member-signup'),
    path('login/', views.login_system, name='login'),
    path('log-out/', views.logout_system, name='log-out'),

]
