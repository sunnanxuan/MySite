from django import forms
from .models import Post, Category, Tag, PostImage
from django.forms import modelformset_factory


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'desc', 'category', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入标题'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入描述', 'rows': 2}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入文章内容', 'rows': 7}),
            'tags': forms.Select(attrs={'class': 'form-control'}),
        }







class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']  # 只需要一个字段来接收图像