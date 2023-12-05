# Ваш urls.py

from django.urls import path
from .views import main
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    # Добавьте другие URL-маршруты, если необходимо
]
