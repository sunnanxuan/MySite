from django.contrib import admin
from django.urls import path, include
from users import views



urlpatterns = [
    path("register/", views.register, name='register'),
    path("login/", views.login, name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("active/<active_code>", views.active_user, name='active_user'),

    path("home/", views.home, name='home'),

]
