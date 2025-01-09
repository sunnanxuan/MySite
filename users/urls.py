from django.contrib import admin
from django.urls import path, include
from users import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("register/", views.register, name='register'),
    path("login/", views.login, name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("active/<active_code>", views.active_user, name='active_user'),
    path("active/", views.active, name='active'),

    path("home/", views.home, name='home'),

    path("user/home/", views.user_home, name='user_home'),
    path("user/profile/", views.user_profile, name='user_profile'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

