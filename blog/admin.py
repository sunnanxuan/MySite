from django.contrib import admin
from blog.models import Category,Post,Tag,Sidebar,Comment
# Register your models here.




admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Sidebar)
admin.site.register(Comment)