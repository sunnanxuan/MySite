from django import forms
from blog.models import Post, Category, Tag
from blog.forms.BootStrap import BootStrapForm





class PostForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = Post
        exclude=['owner', 'is_hot', 'pv','add_date','pub_date','status','liked_users','favorited_users']
        widgets = {
            'category': forms.Select(attrs={'class': 'selectpicker', "data-live-search": 'true'}),
            'tags':forms.SelectMultiple(attrs={'class': 'selectpicker', "data-live-search": 'true', "data-actions-box":"true"}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入描述', 'rows': 2})
        }






