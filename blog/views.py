
from django.shortcuts import render, get_object_or_404,redirect
from .models import Category, Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib import messages



def index(request):
    post_list = Post.objects.filter(status=Post.PUBLISHED)
    context = {'post_list': post_list}
    return render(request, 'index.html', context)




def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    prev_post = Post.objects.filter(id__lt=post_id).order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post_id).order_by('id').first()
    previous_url = request.META.get('HTTP_REFERER', None)

    return render(request, 'post_detail.html', {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        'previous_url': previous_url,
    })






# 展示所有分类
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

# 展示单个分类下的所有博文
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # 仅获取状态为已发布的文章
    posts = Post.objects.filter(category=category, status=Post.PUBLISHED)
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
    #return render(request, 'create_post.html', {'form': form})
    return render(request, 'user.html', {'page_template': 'create_post.html', 'form': form})




@login_required  # 确保只有登录用户才能访问该页面
def my_posts(request):
    # 获取当前用户的博客
    posts = Post.objects.filter(owner=request.user, status=Post.PUBLISHED).order_by('-pub_date')
    return render(request, 'user.html', {'page_template': 'my_posts.html', 'posts': posts})




@login_required
def draft_list(request):
    # 获取当前用户的草稿列表
    drafts = Post.objects.filter(owner=request.user, status=Post.DRAFT).order_by('-add_date')
    return render(request, 'user.html', {'page_template': 'draft_list.html', 'drafts': drafts})



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
    return render(request, 'user.html', {'page_template': 'edit_draft.html', 'form': form, 'draft': draft})




@login_required
def delete_draft(request, post_id):
    draft = get_object_or_404(Post, id=post_id, owner=request.user, status=Post.DRAFT)
    if request.method == 'POST':
        draft.delete()
        messages.success(request, "草稿已成功删除。")
        return redirect('blog:draft_list')
    return HttpResponseForbidden("不允许的操作")