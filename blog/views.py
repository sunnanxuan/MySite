
from django.shortcuts import render, get_object_or_404
from .models import Category, Post
# Create your views here.



def index(request):
    post_list = Post.objects.all()
    context = {'post_list': post_list}
    return render(request, 'index.html', context)




def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})






# 展示所有分类
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

# 展示单个分类下的所有博文
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'posts': posts})
