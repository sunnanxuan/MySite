from django.contrib import admin
from django.urls import path, include
from users.views import account

from django.conf import settings
from django.conf.urls.static import static


app_name = 'users'

urlpatterns = [
    path("register/", account.register, name='register'),
    path("login/", account.login, name='login'),
    path("logout/", account.logout_view, name='logout'),
    path("active/<active_code>", account.active_user, name='active_user'),
    path("active/", account.active, name='active'),

    path("home/", account.user_home, name='user_home'),
    path("profile/", account.user_profile, name='user_profile'),
    path("profile/editor", account.editor_users, name='editor_users'),
    path("account/safety", account.account_safety, name='account_safety'),
    path("account/change/email", account.change_email, name='change_email'),
    path("account/change/password", account.change_password, name='change_password'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

