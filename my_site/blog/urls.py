from django.urls import path
from .views import (
    LikeFilterView,
    PostListView,
    PostSearchView,
    PostDetailView,
    PostCreateView,
    PostListViewTag,
    PostUpdateView,
    PostDeleteView,
    LikeCreateView,
    LikeDeleteView,
    # export_pdf
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('posts/<str:tag>', PostListViewTag.as_view(), name='post-list-tag'),
    path('like/', LikeFilterView.as_view(), name='like-filter'),
    path('search/', PostSearchView.as_view(), name='search_posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/like/', views.LikeCreateView.as_view(), name='like_post'),
    path('post/<int:pk>/unlike/', views.LikeDeleteView.as_view(), name='unlike_post'),
    path('post/<int:pk>/read/', views.PDFView.as_view(), name="read")
]