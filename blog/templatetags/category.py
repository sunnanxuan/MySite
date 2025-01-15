
#在这里自定义模板标签

from django import template
from blog.models import Category,Sidebar,Post

register = template.Library()

@register.simple_tag
def get_category_list():
    return Category.objects.all()



@register.simple_tag
def get_sidebar_list():
    return Sidebar.get_sidebar()



@register.simple_tag
def get_new_post():
    return Post.objects.order_by('-pub_date')[:8]

