from django.urls import path

from users.urls import app_name
from . import views



app_name='blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('categories/', views.category_list, name='category_list'),  # 所有分类列表
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),  # 某个分类的博文
]