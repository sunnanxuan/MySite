
from django.shortcuts import render, get_object_or_404,redirect
from ..models import Category, Post,Comment,PostImage
from ..forms import PostForm, PostImageForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.db.models import Q, F





def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    prev_post = Post.objects.filter(id__lt=post_id).order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post_id).order_by('id').first()
    Post.objects.filter(id=post_id).update(pv=F('pv') + 1)  # 增加浏览量
    previous_url = request.META.get('HTTP_REFERER', None)

    # 获取文章关联的图片
    images = post.images.all()

    return render(request, 'post_detail.html', {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        'images': images,  # 将图片传递到模板
        'previous_url': previous_url,
    })



@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        image_form = PostImageForm(request.POST, request.FILES)

        # 检查文章表单是否有效
        if post_form.is_valid():
            # 保存文章内容
            post = post_form.save(commit=False)
            post.owner = request.user


            # 检查是否点击了发布按钮
            if 'publish' in request.POST:
                post.status = Post.PUBLISHED  # 设置文章状态为发布
            else:
                post.status = Post.DRAFT  # 如果没有点击发布按钮，设置为草稿

            post.save()

            tags = request.POST.getlist('tags')  # 获取选中的标签 ID 列表
            post.tags.set(tags)  # 将选中的标签与文章关联
            post.save()

            # 获取上传的所有图片文件
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')  # 获取所有上传的图片文件

                # 保存每张图片到数据库
                for image in images:
                    PostImage.objects.create(post=post, image=image)

            # 返回成功响应
            return JsonResponse({'success': True})

    else:
        post_form = PostForm()
        image_form = PostImageForm()

    return render(request, 'create_post.html', {'post_form': post_form, 'image_form': image_form})




@login_required
def edit_post(request, post_id):
    # 获取已发布的文章
    post = get_object_or_404(Post, id=post_id, owner=request.user, status=Post.PUBLISHED)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        image_form = PostImageForm(request.POST, request.FILES)

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

            # 删除图片操作
            if 'delete_image' in request.POST:
                delete_image_ids = request.POST.get('delete_image', '').split(',')
                for image_id in filter(None, delete_image_ids):
                    image = get_object_or_404(PostImage, id=image_id)
                    image.delete()

            # 保存新的图片文件
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for image in images:
                    PostImage.objects.create(post=post, image=image)

            # 返回成功响应
            return JsonResponse({'success': True})

    else:
        form = PostForm(instance=post)
        image_form = PostImageForm()

    return render(request, 'edit_post.html', {
        'form': form,
        'post': post,
        'image_form': image_form,
        'active_menu': 'content-manage',
        'active_link': 'published_posts'
    })



def delete_image(request, image_id):
    if request.method == 'DELETE':
        image = get_object_or_404(PostImage, id=image_id)
        image.delete()
        return JsonResponse({'status': 'success'})





@login_required
def draft_list(request):
    # 获取当前用户的草稿列表
    drafts = Post.objects.filter(owner=request.user, status=Post.DRAFT).order_by('-add_date')
    return render(request, 'draft_list.html', { 'drafts': drafts, 'active_menu': 'content-manage', 'active_link': 'draft_list'})




@login_required
def edit_draft(request, post_id):
    # 获取当前用户的草稿
    draft = get_object_or_404(Post, id=post_id, owner=request.user, status=Post.DRAFT)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=draft)
        image_form = PostImageForm(request.POST, request.FILES)


        if form.is_valid():
            # 保存文章内容
            post = form.save(commit=False)
            post.owner = request.user

            # 检查是否点击了发布按钮
            if 'publish' in request.POST:
                post.status = Post.PUBLISHED  # 设置文章状态为发布

            post.save()

            tags = request.POST.getlist('tags')  # 获取选中的标签 ID 列表
            post.tags.set(tags)  # 将选中的标签与文章关联
            post.save()


            if 'delete_image' in request.POST:
                delete_image_ids = request.POST.get('delete_image', '').split(',')
                for image_id in filter(None, delete_image_ids):
                    image = get_object_or_404(PostImage, id=image_id)
                    image.delete()

            # 获取上传的所有图片文件
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')  # 获取所有上传的图片文件

                # 保存每张图片到数据库
                for image in images:
                    PostImage.objects.create(post=post, image=image)

            # 返回成功响应
            return JsonResponse({'success': True})

    else:
        form = PostForm(instance=draft)
        image_form = PostImageForm()

    return render(request, 'edit_draft.html', {
        'form': form,
        'draft': draft,
        'image_form': image_form,
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
    # 获取用户评论过的博客
    commented_post_ids = Comment.objects.filter(user=user).values_list('post_id', flat=True).distinct()
    posts = Post.objects.filter(id__in=commented_post_ids)

    return render(
        request,
        'users/commented_posts.html',
        {
            'posts': posts,
            'active_menu': 'user-info',  # 设置当前活动的菜单
            'active_link': 'my_posts',  # 设置当前活动的链接
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


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, owner=request.user, status=Post.PUBLISHED)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "文章已成功删除。")
        return redirect('blog:my_posts')
    return HttpResponseForbidden("不允许的操作")