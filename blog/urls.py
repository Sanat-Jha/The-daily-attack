from django.urls import path
from . import views
from . import views_api

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tag/<str:tag_name>/', views.tag_posts, name='tag_posts'),
    path('search/', views.search_posts, name='search_posts'),
    
    # API endpoints for Gemini integration
    path('api/title-suggestions/', views_api.api_title_suggestions, name='api_title_suggestions'),
    path('api/content-suggestions/', views_api.api_content_suggestions, name='api_content_suggestions'),
]