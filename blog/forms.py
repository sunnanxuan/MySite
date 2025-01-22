from django import forms
from .models import Post, Category, Tag, PostImage



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'desc', 'category', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入标题'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入描述', 'rows': 2}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入文章内容', 'rows': 7}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),  # 修改为 SelectMultiple 以支持多选
        }






class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']  # 只需要一个字段来接收图像