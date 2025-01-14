
from django.shortcuts import render, get_object_or_404,redirect
from .models import Category, Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
# Create your views here.



def index(request):
    post_list = Post.objects.all()
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
    posts = Post.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'posts': posts})



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user  # 设置文章作者为当前登录用户
            post.save()
            return redirect('blog:index')  # 发布成功后跳转到首页
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})
