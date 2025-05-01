from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from .models import Post, APIKey, Tag
from .serializers import PostSerializer, PostCreateSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication

class IsAPIKeyAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return False
        
        try:
            api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
            # Set the user on the request
            request.user = api_key_obj.user
            return True
        except APIKey.DoesNotExist:
            return False

@api_view(['GET'])
def api_posts_list(request):
    """
    List all published posts
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    posts = Post.objects.filter(status='published').order_by('-published_at')
    posts_data = []
    
    for post in posts:
        posts_data.append({
            'id': post.pk,
            'title': post.title,
            'content': post.content,
            'status': post.status,
            'created_at': post.created_at.isoformat() if post.created_at else None,
            'published_at': post.published_at.isoformat() if post.published_at else None,
            'author': post.author.username,
            'tags': [{'name': tag.name} for tag in post.tags.all()]
        })
    
    return JsonResponse(posts_data, safe=False)

@api_view(['GET'])
def api_posts_search(request):
    """
    Search for published posts matching a query
    """
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'Search query is required'}, status=400)
    
    # Search in title and content
    from django.db.models import Q
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        status='published'
    ).order_by('-published_at')
    
    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.pk,
            'title': post.title,
            'content': post.content,
            'status': post.status,
            'created_at': post.created_at.isoformat() if post.created_at else None,
            'published_at': post.published_at.isoformat() if post.published_at else None,
            'author': post.author.username,
            'tags': [{'name': tag.name} for tag in post.tags.all()]
        })
    
    return JsonResponse(posts_data, safe=False)

@api_view(['GET'])
def api_post_detail(request, pk):
    """
    Retrieve a specific published post
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    post = get_object_or_404(Post, pk=pk, status='published')
    
    post_data = {
        'id': post.pk,
        'title': post.title,
        'content': post.content,
        'status': post.status,
        'created_at': post.created_at.isoformat() if post.created_at else None,
        'published_at': post.published_at.isoformat() if post.published_at else None,
        'author': post.author.username,
        'tags': [{'name': tag.name} for tag in post.tags.all()]
    }
    
    return JsonResponse(post_data)

@api_view(['POST'])
@permission_classes([IsAPIKeyAuthenticated])
@csrf_exempt
def api_post_create(request):
    """
    Create a new post (requires API key)
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Check API key directly instead of using the permission class
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return JsonResponse({'error': 'API key is required'}, status=401)
    
    try:
        api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
        user = api_key_obj.user
    except APIKey.DoesNotExist:
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Validate required fields
    if 'title' not in data or 'content' not in data:
        return JsonResponse({'error': 'Title and content are required'}, status=400)
    
    # Create post
    post = Post(
        title=data['title'],
        content=data['content'],
        status=data.get('status', 'draft'),
        author=user
    )
    
    # Set published_at if status is published
    if post.status == 'published':
        from django.utils import timezone
        post.published_at = timezone.now()
    
    post.save()
    
    # Add tags if provided
    if 'tags' in data and isinstance(data['tags'], list):
        for tag_name in data['tags']:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip().lower())
            post.tags.add(tag)
    
    # Return the created post
    post_data = {
        'id': post.pk,
        'title': post.title,
        'content': post.content,
        'status': post.status,
        'created_at': post.created_at.isoformat() if post.created_at else None,
        'published_at': post.published_at.isoformat() if post.published_at else None,
        'author': post.author.username,
        'tags': [{'name': tag.name} for tag in post.tags.all()]
    }
    
    return JsonResponse(post_data, status=201)

# Add these functions for Gemini integration
@csrf_exempt
def api_title_suggestions(request):
    """
    Generate title suggestions using AI
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        topic = data.get('topic', '')
        keywords = data.get('keywords', [])
        
        if not topic:
            return JsonResponse({'error': 'Topic is required'}, status=400)
        
        # For now, return some dummy suggestions
        # In a real implementation, this would call Gemini API
        suggestions = [
            f"The Ultimate Guide to {topic}",
            f"{topic}: What You Need to Know in 2023",
            f"How {topic} is Changing the Future",
            f"10 Ways to Master {topic} Today",
            f"Understanding {topic}: A Comprehensive Analysis"
        ]
        
        return JsonResponse({'suggestions': suggestions})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
def api_content_suggestions(request):
    """
    Generate content suggestions using AI
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        title = data.get('title', '')
        outline = data.get('outline', [])
        
        if not title:
            return JsonResponse({'error': 'Title is required'}, status=400)
        
        # For now, return some dummy content
        # In a real implementation, this would call Gemini API
        content = f"""
<h1>{title}</h1>

<p>This is an introduction to {title}. It provides context and background information.</p>

<h2>Key Points</h2>
<p>Here are some important aspects to consider:</p>
<ul>
    <li>First key point about {title}</li>
    <li>Second key point with more details</li>
    <li>Third key point with analysis</li>
</ul>

<h2>Analysis</h2>
<p>This section provides deeper analysis of {title} and its implications.</p>

<h2>Conclusion</h2>
<p>In conclusion, {title} represents an important topic that deserves attention and further study.</p>
"""
        
        return JsonResponse({'content': content})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

def api_docs(request):
    """
    Display API documentation
    """
    return render(request, 'blog/api_docs.html')