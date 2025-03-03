
from django.shortcuts import render, get_object_or_404,redirect

from users.models import Follow
from ..models import Category, Post,Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from utils.pagination import Pagination



@login_required
def my_posts(request):
    post_list = Post.objects.filter(owner=request.user, status=Post.PUBLISHED).order_by('-pub_date')
    total_count = post_list.count()
    page = request.GET.get('page', 1)
    per_page = 5

    # 使用自定义分页插件
    pagination = Pagination(page, total_count, request.path_info, request.GET, per_page=per_page)
    posts = post_list[pagination.start:pagination.end]
    page_html = pagination.page_html()

    return render(
        request,
        'users/my_posts.html',
        {
            'posts': posts,              # 分页后的文章列表
            'active_menu': 'user-info',    # 当前活动的菜单
            'active_link': 'my_posts',     # 当前活动的链接
            'page_html': page_html,        # 分页插件生成的 HTML
        }
    )



@login_required
def favorited_posts(request):
    user = request.user
    # 先按发布时间倒序排序收藏的博客
    post_list = Post.objects.filter(favorited_users=user).order_by('-pub_date')
    total_count = post_list.count()
    page = request.GET.get('page', 1)
    per_page = 5  # 每页显示 5 篇文章

    # 使用自定义分页插件
    pagination = Pagination(page, total_count, request.path_info, request.GET, per_page=per_page)
    posts = post_list[pagination.start:pagination.end]
    page_html = pagination.page_html()

    return render(
        request,
        'users/favorited_posts.html',
        {
            'posts': posts,              # 分页后的文章列表
            'page_html': page_html,        # 分页插件生成的 HTML
            'active_menu': 'user-info',    # 当前活动的菜单
            'active_link': 'favorited_posts',  # 当前活动的链接（请根据需要调整）
        }
    )




@login_required
def liked_posts(request):
    user = request.user
    post_list = Post.objects.filter(liked_users=user).order_by('-pub_date')
    total_count = post_list.count()
    page = request.GET.get('page', 1)
    per_page = 5

    # 使用自定义分页插件
    pagination = Pagination(page, total_count, request.path_info, request.GET, per_page=per_page)
    posts = post_list[pagination.start:pagination.end]
    page_html = pagination.page_html()

    return render(
        request,
        'users/liked_posts.html',
        {
            'posts': posts,              # 分页后的文章列表
            'page_html': page_html,        # 分页插件生成的 HTML
            'active_menu': 'user-info',    # 设置当前活动的菜单
            'active_link': 'liked_posts',  # 设置当前活动的链接（可根据实际情况调整）
        }
    )







def author_profile(request, author_id):
    # 获取作者用户
    author = get_object_or_404(User, id=author_id)

    # 获取作者发布的文章
    posts = Post.objects.filter(owner=author, status='published').order_by('-pub_date')

    # 添加分页
    paginator = Paginator(posts, 8)  # 每页显示 8 篇文章
    page_number = request.GET.get('page')
    post_list = paginator.get_page(page_number)

    # 获取所有关注该作者的用户
    followers = User.objects.filter(following__followed=author)

    # 判断当前登录用户是否关注了该作者
    is_following = False
    if request.user.is_authenticated:  # 确保用户已登录
        is_following = Follow.objects.filter(follower=request.user, followed=author).exists()

    # 渲染模板
    return render(request, 'users/author_profile.html', {
        'author': author,
        'post_list': post_list,
        'followers': followers,
        'is_following': is_following,  # 当前用户是否关注作者
    })





@login_required
def received_comments(request):
    # 获取当前用户的所有文章
    posts = Post.objects.filter(owner=request.user)

    # 获取所有评论过这些文章的评论
    comments = Comment.objects.filter(post__in=posts).order_by('-created_at')

    context = {
        'comments': comments,
        'active_menu': 'comment',
        'active_link': 'comment'
    }
    return render(request, 'users/received_comments.html', context)







