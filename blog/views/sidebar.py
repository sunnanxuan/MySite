from django.shortcuts import render, get_object_or_404,redirect
from ..models import Category, Post,Comment,PostImage
from ..forms import PostForm, PostImageForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def search(request):
    keywords = request.GET.get('keywords')
    if not keywords:
        post_list = Post.objects.all()
    else:
        post_list = Post.objects.filter(
            Q(title__icontains=keywords) | Q(content__icontains=keywords) | Q(desc__icontains=keywords),
            status=Post.PUBLISHED
        )
    context = {'post_list': post_list}

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



