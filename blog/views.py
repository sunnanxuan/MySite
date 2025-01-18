
from django.shortcuts import render, get_object_or_404,redirect
from .models import Category, Post,Comment
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.db.models import Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


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


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    prev_post = Post.objects.filter(id__lt=post_id).order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post_id).order_by('id').first()
    Post.objects.filter(id=post_id).update(pv=F('pv')+1) #此方法有bug，暂时这样仅做此路
    previous_url = request.META.get('HTTP_REFERER', None)

    return render(request, 'post_detail.html', {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
    })






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



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            if 'save_draft' in request.POST:
                post.status = Post.DRAFT
            else:
                post.status = Post.PUBLISHED
            post.save()
            return redirect('blog:index')
    else:
        form = PostForm()
    return render(request, 'user.html', {'page_template': 'create_post.html', 'form': form, 'active_menu': 'content-manage', 'active_link': 'create_post'})




@login_required  # 确保只有登录用户才能访问该页面
def my_posts(request):
    # 获取当前用户的博客
    posts = Post.objects.filter(owner=request.user, status=Post.PUBLISHED).order_by('-pub_date')
    return render(request, 'user.html', {'page_template': 'my_posts.html', 'posts': posts, 'active_menu': 'content-manage', 'active_link': 'my_posts'})




@login_required
def draft_list(request):
    # 获取当前用户的草稿列表
    drafts = Post.objects.filter(owner=request.user, status=Post.DRAFT).order_by('-add_date')
    return render(request, 'user.html', {'page_template': 'draft_list.html', 'drafts': drafts, 'active_menu': 'content-manage', 'active_link': 'draft_list'})



@login_required
def edit_draft(request, post_id):
    # 获取当前用户的草稿
    draft = get_object_or_404(Post, id=post_id, owner=request.user, status=Post.DRAFT)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=draft)
        if form.is_valid():
            # 根据提交按钮的值决定操作
            if 'publish' in request.POST:  # 点击发布按钮
                draft.status = Post.PUBLISHED
                draft.pub_date = timezone.now()
            elif 'save_draft' in request.POST:  # 点击保存草稿按钮
                draft.status = Post.DRAFT
            draft.save()
            return redirect('blog:draft_list')  # 跳转到草稿箱页面
    else:
        form = PostForm(instance=draft)
    #return render(request, 'edit_draft.html', {'form': form, 'draft': draft})
    return render(request, 'user.html', {'page_template': 'edit_draft.html', 'form': form, 'draft': draft, 'active_menu': 'content-manage', 'active_link': 'draft_list'})




@login_required
def delete_draft(request, post_id):
    draft = get_object_or_404(Post, id=post_id, owner=request.user, status=Post.DRAFT)
    if request.method == 'POST':
        draft.delete()
        messages.success(request, "草稿已成功删除。")
        return redirect('blog:draft_list')
    return HttpResponseForbidden("不允许的操作")



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
    return render(request, 'archives_list.html', context)




@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
            messages.success(request, "评论提交成功！")
        else:
            messages.error(request, "评论内容不能为空！")
    return redirect("blog:post_detail", post_id=post_id)



@login_required
def like_post(request, post_id):
    """点赞博客"""
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.liked_users.all():
        post.liked_users.remove(request.user)  # 取消点赞
        liked = False
    else:
        post.liked_users.add(request.user)  # 添加点赞
        liked = True
    return JsonResponse({"liked": liked, "total_likes": post.total_likes()})



@login_required
def favorite_post(request, post_id):
    """收藏博客"""
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.favorited_users.all():
        post.favorited_users.remove(request.user)  # 取消收藏
        favorited = False
    else:
        post.favorited_users.add(request.user)  # 添加收藏
        favorited = True
    return JsonResponse({"favorited": favorited, "total_favorites": post.total_favorites()})