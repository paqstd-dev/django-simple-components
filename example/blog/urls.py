from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('posts/', views.posts_view, name='posts'),
    path('posts/<int:post_id>/', views.post_view, name='post'),
]
