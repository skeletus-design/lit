import datetime
from typing import Any
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    RedirectView,
)



# from blog.forms import ImageForm
from .models import Post, Likes
from .admin import PostAdmin, site
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
8# from .forms import PostCreateForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q



def home(request, self):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class LikeFilterView(ListView):
    model = Post
    template_name = 'blog/home.html'  
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
    # Likes.objects.annotate(num_likes=Count('post_key')).order_by('-like_key')
    

class LikeCreateView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        self.create_like()
        return reverse('post-detail', kwargs={
            "pk": self.get_post().pk
        })
    
    def get_post(self):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        return post
    
    def create_like(self):
        user = self.request.user
        post = self.get_post()  
              
        likes, is_created = Likes.objects.get_or_create(
            post_key=post,
            user_key=user
        )
        
        return likes
    

class LikeDeleteView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        self.delete_like()
        return reverse('post-detail', kwargs={
            "pk": self.get_post().pk
        })
    
    def get_post(self):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        return post
    
    def delete_like(self):
        user = self.request.user
        post = self.get_post()
        
        like = Likes.objects.filter(post_key=post, user_key=user)
        if like:
            like.delete()
        
        return
        

# def index(request):
#     serch_querry = request.GET.get("q")
#     groups = Post.objects.all()
    
#     if serch_querry == None

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  
    context_object_name = 'posts'
    ordering = ['-date_posted']

    
    
    
class PostSearchView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
    def get_queryset(self, *args, **kwargs):
        try:
            queryset = super().get_queryset(*args, **kwargs)
            search_query = self.request.GET.get('q')
        
            if not search_query:
                messages.error(request=self.request, message='Ошибка поиска: запрос не указан.')
                return []
            
        except:
            messages.error(request=self.request, message='Ошибка поиска')
               
        model_admin = PostAdmin(self.model, site)
        search_queryset, _ =  model_admin.get_search_results(request=self.request, queryset=queryset, search_term=search_query)
        return search_queryset
    
        
# Фильтр тегов
class PostListViewTag(ListView):
    model = Post
    template_name = 'blog/home.html'  
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
    # пример фильтрации
    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return super().get_queryset().filter(tag=tag)
    

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'object'
    fields = ['title', 'content', 'image','tag']
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        post_object = self.get_object()
        user = self.request.user
        
        context_data[self.context_object_name] = post_object
        context_data['user_like'] = Likes.objects.filter(post_key=post_object, user_key=user)
        return context_data
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'pdf', 'tag',]
    # @method_decorator(csrf_exempt)
    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            return super().form_valid(form)
        except:
            
            messages.error(request=self.request, message='Ошибка')
    
    
# def form_valid(self, form):
    
    
# def SaveImage(request):
#     if request.method == 'POST':
#         p_form = ImageForm(request.POST,
#                                    request.FILES,
#                                    instance=request.user.profile)
#         if p_form.is_valid():
#             p_form.save()
#             return redirect('post-update')    
        
#     context = {
#         'p_form': p_form
#     }
#     return render(request, 'post-update', context)
        


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'tag']
    # @method_decorator(csrf_exempt)
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # @method_decorator(csrf_exempt)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    # @method_decorator(csrf_exempt)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'О книге рецептов'})

from django.http import FileResponse, Http404


class PDFView(View):
    model = Post
    context_object_name = 'object'
    
    def get(self, request, *args, **kwargs):
        object_pk = kwargs.get('pk')
        object_instance = self.model.objects.get(pk=object_pk)
        
        try:
            return FileResponse(open(object_instance.pdf.path, 'rb'), content_type='uploads/pdf')
        except FileNotFoundError:
            raise Http404()