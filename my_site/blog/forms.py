from django import forms
# from django.contrib.auth.models import 
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class LikeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['likes']
# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['image']