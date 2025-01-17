from django.urls import path

from users.urls import app_name
from . import views



app_name='blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('categories/', views.category_list, name='category_list'),  # 所有分类列表
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),  # 某个分类的博文

    path('create/', views.create_post, name='create_post'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('drafts/', views.draft_list, name='draft_list'),  # 草稿箱
    path('drafts/edit/<int:post_id>/', views.edit_draft, name='edit_draft'),
    path('drafts/delete/<int:post_id>/', views.delete_draft, name='delete_draft'),
    path('search/', views.search, name='search'),
    path('archives/<int:year>/<int:month>/', views.archives, name='archives'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),

]