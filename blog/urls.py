from django.urls import path

from users.urls import app_name
from . import views



app_name='blog'
urlpatterns = [
    path('', views.index, name='index'),
]