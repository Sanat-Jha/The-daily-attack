from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tag/<str:tag_name>/', views.tag_posts, name='tag_posts'),
    path('search/', views.search_posts, name='search_posts'),
    # Add a direct link to create a new post
    path('create/', views.post_new, name='create_post'),
    path('check-status/', views.check_user_status, name='check_user_status'),
]