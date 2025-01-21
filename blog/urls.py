from django.urls import path

from users.urls import app_name
from .views import user,index,post,sidebar



app_name='blog'
urlpatterns = [
    path('', index.index, name='index'),
    path('post/<int:post_id>/', post.post_detail, name='post_detail'),
    path('categories/', index.category_list, name='category_list'),  # 所有分类列表
    path('category/<int:category_id>/', index.category_detail, name='category_detail'),  # 某个分类的博文

    path('create/', post.create_post, name='create_post'),

    path('my-posts/', user.my_posts, name='my_posts'),
    path('favorited/', user.favorited_posts, name='favorited_posts'),
    path('liked/', user.liked_posts, name='liked_posts'),
    path('commented/', post.commented_posts, name='commented_posts'),

    path('drafts/', post.draft_list, name='draft_list'),  # 草稿箱
    path('drafts/edit/<int:post_id>/', post.edit_draft, name='edit_draft'),
    path('delete_image/<int:image_id>/', post.delete_image, name='delete_image'),
    path('drafts/delete/<int:post_id>/', post.delete_draft, name='delete_draft'),

    path('search/', sidebar.search, name='search'),
    path('archives/<int:year>/<int:month>/', sidebar.archives, name='archives'),

    path('post/<int:post_id>/comment/', post.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', post.like_post, name='like_post'),
    path('post/<int:post_id>/favorite/', post.favorite_post, name='favorite_post'),

    path('author/<int:author_id>/', user.author_profile, name='author_profile'),

    path('my-posts/delete/<int:post_id>/', post.delete_post, name='delete_post'),

    path('post/edit/<int:post_id>/', post.edit_post, name='edit_post'),

]