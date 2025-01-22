from django.shortcuts import render, get_object_or_404,redirect
from ..models import Category, Post,Comment,PostImage, Tag
from ..forms import PostForm, PostImageForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def search(request):
    query = request.GET.get('query')
    if not query:
        # 如果没有输入查询关键字，显示所有文章
        post_list = Post.objects.all()
    else:
        # 根据标题、内容、描述模糊匹配
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(desc__icontains=query),
            status=Post.PUBLISHED
        )
    context = {'post_list': post_list, 'search_type': 'keyword'}
    return render(request, 'index.html', context)




def archives(request, year, month):
    post_queryset = Post.objects.filter(
        status=Post.PUBLISHED,
        add_date__year=year,
        add_date__month=month
    )

    # 分页
    paginator = Paginator(post_queryset, 5)  # 每页 5 篇文章
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'year': year, 'month': month}
    return render(request, 'sidebar/archives_list.html', context)




def tag_search(request):
    query = request.GET.get('query')
    if not query:
        # 如果没有输入查询关键字，显示所有文章
        post_list = Post.objects.filter(status=Post.PUBLISHED)
    else:
        # 根据标签名称进行搜索
        post_list = Post.objects.filter(
            tags__name__icontains=query,
            status=Post.PUBLISHED
        ).distinct()
    context = {'post_list': post_list, 'search_type': 'tag'}
    return render(request, 'index.html', context)