
from django.shortcuts import render, get_object_or_404,redirect
from ..models import Post,Comment
from blog.forms.post import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.db.models import F
from utils.send_system_message import send_system_message
from django.urls import reverse
from utils.pagination import Pagination







def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    prev_post = Post.objects.filter(id__lt=post_id).order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post_id).order_by('id').first()
    Post.objects.filter(id=post_id).update(pv=F('pv') + 1)  # 增加浏览量
    previous_url = request.META.get('HTTP_REFERER', None)

    return render(request, 'post_detail.html', {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        'previous_url': previous_url,
    })




@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.owner = request.user
            if 'publish' in request.POST:
                post.status = Post.PUBLISHED
                url = reverse('blog:post_detail', args=[post.id])
            else:
                post.status = Post.DRAFT
                url = reverse('blog:draft_list')
            post.save()
            tags = request.POST.getlist('tags')
            post.tags.set(tags)
            return JsonResponse({'success': True, 'url': url})
        else:
            return JsonResponse({'success': False, 'error': post_form.errors})
    else:
        post_form = PostForm()
    return render(request, 'post/create_post.html', {'form': post_form,'active_menu': 'content-manage',
        'active_link': 'create_post'})







@login_required
def edit_post(request, post_id):
    # 获取已发布的文章
    post = get_object_or_404(Post, id=post_id, owner=request.user, status=Post.PUBLISHED)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            # 保存文章内容
            post = form.save(commit=False)
            post.owner = request.user

            # 检查是否点击了发布按钮
            if 'publish' in request.POST:
                post.status = Post.PUBLISHED  # 保证状态为发布

            post.save()

            tags = request.POST.getlist('tags')  # 获取选中的标签 ID 列表
            post.tags.set(tags)  # 将选中的标签与文章关联
            post.save()

            url = reverse('blog:post_detail', args=[post.id])
            return JsonResponse({'success': True, 'url': url})

    else:
        form = PostForm(instance=post)

    return render(request, 'post/edit_post.html', {
        'form': form,
        'post': post,
        'active_menu': 'user-info',
        'active_link': 'my_posts'
    })






@login_required
def draft_list(request):
    # 获取当前用户的草稿列表
    draft_queryset = Post.objects.filter(owner=request.user, status=Post.DRAFT).order_by('-add_date')
    total_count = draft_queryset.count()
    page = request.GET.get('page', 1)
    per_page = 10  # 每页显示 5 篇草稿

    # 使用自定义分页插件
    pagination = Pagination(page, total_count, request.path_info, request.GET, per_page=per_page)
    drafts = draft_queryset[pagination.start:pagination.end]
    page_html = pagination.page_html()

    return render(
        request,
        'draft_list.html',
        {
            'drafts': drafts,        # 分页后的草稿列表
            'page_html': page_html,    # 分页插件生成的 HTML
            'active_menu': 'content-manage',
            'active_link': 'draft_list'
        }
    )




@login_required
def edit_draft(request, post_id):
    # 获取当前用户的草稿
    draft = get_object_or_404(Post, id=post_id, owner=request.user, status=Post.DRAFT)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=draft)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            # 根据提交按钮确定状态和跳转 URL
            if 'publish' in request.POST:
                post.status = Post.PUBLISHED
                url = reverse('blog:post_detail', args=[post.id])
            else:
                post.status = Post.DRAFT
                url = reverse('blog:draft_list')
            post.save()
            tags = request.POST.getlist('tags')
            post.tags.set(tags)
            post.save()
            return JsonResponse({'success': True, 'url': url})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    else:
        form = PostForm(instance=draft)

    return render(request, 'post/edit_draft.html', {
        'form': form,
        'draft': draft,
        'active_menu': 'content-manage',
        'active_link': 'draft_list'
    })




def delete_draft(request, post_id):
    draft = get_object_or_404(Post, id=post_id, owner=request.user, status=Post.DRAFT)
    if request.method == 'POST':
        draft.delete()
        messages.success(request, "草稿已成功删除。")
        return redirect('blog:draft_list')
    return HttpResponseForbidden("不允许的操作")



@login_required
def commented_posts(request):
    user = request.user
    # 获取用户评论过的博客ID，并按照发布时间倒序排序
    commented_post_ids = Comment.objects.filter(user=user).values_list('post_id', flat=True).distinct()
    post_list = Post.objects.filter(id__in=commented_post_ids).order_by('-pub_date')
    total_count = post_list.count()
    page = request.GET.get('page', 1)
    per_page = 5  # 每页显示 5 篇文章

    # 使用自定义分页插件
    pagination = Pagination(page, total_count, request.path_info, request.GET, per_page=per_page)
    posts = post_list[pagination.start:pagination.end]
    page_html = pagination.page_html()

    return render(
        request,
        'users/commented_posts.html',
        {
            'posts': posts,              # 分页后的文章列表
            'page_html': page_html,        # 分页插件生成的 HTML
            'active_menu': 'user-info',    # 当前活动的菜单
            'active_link': 'commented_posts',  # 当前活动的链接（请根据需要调整）
        }
    )





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

    # 给文章作者发送点赞通知
    if liked:
        message = f"您的文章《{post.title}》被{request.user.username}点赞了！"
        send_system_message(post.owner, message)

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

    # 给文章作者发送收藏通知
    if favorited:
        message = f"您的文章《{post.title}》被{request.user.username}收藏了！"
        send_system_message(post.owner, message)

    return JsonResponse({"favorited": favorited, "total_favorites": post.total_favorites()})




def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, owner=request.user, status=Post.PUBLISHED)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "文章已成功删除。")
        return redirect('blog:my_posts')
    return HttpResponseForbidden("不允许的操作")


