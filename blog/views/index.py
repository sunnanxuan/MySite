
from django.shortcuts import render, get_object_or_404,redirect
from blog.models import Category, Post,Comment,Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def index(request):
    # 获取已发布的文章
    post_list = Post.objects.filter(status=Post.PUBLISHED)

    # 设置每页显示文章数
    paginator = Paginator(post_list, 5)  # 每页 5 篇文章
    page = request.GET.get('page')  # 获取当前页码

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # 如果页码不是整数，返回第一页
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # 如果超出页码范围，返回最后一页

    # 渲染模板并传递分页后的文章列表
    context = {'post_list': posts}
    return render(request, 'index.html', context)





# 展示所有分类
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

# 展示单个分类下的所有博文
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # 仅获取状态为已发布的文章
    post_list = Post.objects.filter(category=category, status=Post.PUBLISHED)

    # 分页逻辑
    paginator = Paginator(post_list, 5)  # 每页显示5篇文章
    page = request.GET.get('page', 1)  # 获取当前页码
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，返回最后一页
        posts = paginator.page(paginator.num_pages)

    return render(request, 'category_detail.html', {'category': category, 'posts': posts})

















