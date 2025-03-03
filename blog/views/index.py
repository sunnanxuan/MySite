
from django.shortcuts import render, get_object_or_404,redirect
from blog.models import Category, Post,Comment,Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.pagination import Pagination




def index(request):
    # 获取已发布的文章
    post_list = Post.objects.filter(status=Post.PUBLISHED)
    total_count = post_list.count()
    page = request.GET.get('page', 1)  # 如果没有提供则默认为第一页
    per_page = 5  # 每页显示 5 篇文章

    # 使用自定义分页插件（请确保 Pagination 类已正确导入）
    pagination = Pagination(page, total_count, request.path_info, request.GET, per_page=per_page)
    posts = post_list[pagination.start:pagination.end]
    page_html = pagination.page_html()

    context = {
        'post_list': posts,   # 分页后的文章列表
        'page_html': page_html  # 分页插件生成的 HTML
    }
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

















