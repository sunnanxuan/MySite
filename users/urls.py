from django.contrib import admin
from django.urls import path, include
from users.views import account, users

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

    path('<int:recipient_id>/message/', users.send_message_view, name='send_message'),
    path('inbox/', users.inbox_view, name='inbox'),
    path('message/<int:message_id>/', users.read_message, name='read_message'),

    path('<int:user_id>/follow/', users.follow_user, name='follow_user'),

    path('following/', users.my_following, name='my_following'),
    path('followers/', users.my_followers, name='my_followers'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

