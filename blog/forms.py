from django import forms
from .models import Post, Category, Tag, PostImage
from django.forms import modelformset_factory



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'desc', 'category', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入标题'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入描述', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入文章内容', 'rows': 8}),
            'tags': forms.Select(attrs={'class': 'form-control'}),
        }




class PostImageForm(forms.ModelForm):
    """图片上传表单"""
    class Meta:
        model = PostImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# 使用 modelformset_factory 生成图片表单集
PostImageFormSet = modelformset_factory(
    PostImage,
    form=PostImageForm,
    extra=3,  # 默认支持上传 3 张图片
    can_delete=True  # 允许删除图片
)