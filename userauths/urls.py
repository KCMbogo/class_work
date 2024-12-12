from django.urls import path
from userauths import views
from django.contrib.auth.views import LogoutView


app_name = 'userauths'

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
]


    