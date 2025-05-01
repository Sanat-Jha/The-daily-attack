from django.urls import path
from . import views
from . import views_api
from . import api_views

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
    
    # API documentation
    path('api/docs/', views.api_docs, name='api_docs'),
    
    # API endpoints
    path('api/posts/', api_views.api_posts_list, name='api_posts_list'),
    path('api/posts/search/', api_views.api_posts_search, name='api_posts_search'),
    path('api/posts/<int:pk>/', api_views.api_post_detail, name='api_post_detail'),
    path('api/posts/create/', api_views.api_post_create, name='api_post_create'),
]