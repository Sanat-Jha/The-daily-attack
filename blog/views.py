from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from .models import Post, Tag, UserProfile
from .forms import SignUpForm, PostForm
from .decorators import editor_required

def home(request):
    posts = Post.objects.filter(status='published')
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.status == 'draft' and (not request.user.is_authenticated or 
                                   not hasattr(request.user, 'profile') or 
                                   request.user.profile.user_type != 'editor' or 
                                   request.user != post.author):
        messages.error(request, "You don't have permission to view this draft post.")
        return redirect('home')
    return render(request, 'blog/post_detail.html', {'post': post})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a UserProfile with viewer type by default
            UserProfile.objects.create(user=user, user_type='viewer')
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    if hasattr(request.user, 'profile') and request.user.profile.user_type == 'editor':
        # For editors, show all their posts (both published and drafts)
        posts = Post.objects.filter(author=request.user).order_by('-created_at')
    else:
        # For viewers, only show published posts
        posts = Post.objects.filter(status='published')
    return render(request, 'blog/dashboard.html', {'posts': posts})

@login_required
@editor_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.status == 'published':
                post.published_at = timezone.now()
            post.save()
            
            # Handle tags separately after saving the post
            tag_names = form.cleaned_data.get('tags', [])
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)
                
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
@editor_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if post.status == 'published' and not post.published_at:
                post.published_at = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        # Prepare tags for the form
        tags = ', '.join([tag.name for tag in post.tags.all()])
        form = PostForm(instance=post, initial={'tags': tags})
    
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
@editor_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the user is the author
    if post.author != request.user:
        messages.error(request, "You can only publish your own posts.")
        return redirect('post_detail', pk=post.pk)
    
    post.status = 'published'
    post.published_at = timezone.now()
    post.save()
    
    messages.success(request, "Your post has been published!")
    
    # Check if the user wants to share to LinkedIn
    share_to_linkedin = request.GET.get('share_to_linkedin', 'false') == 'true'
    
    if share_to_linkedin:
        # Redirect to LinkedIn post creation page
        return redirect('https://www.linkedin.com/post/new')
    
    return redirect('post_detail', pk=post.pk)

def tag_posts(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags=tag, status='published')
    return render(request, 'blog/home.html', {'posts': posts, 'tag': tag})

def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        )
    else:
        posts = Post.objects.filter(status='published')
    return render(request, 'blog/home.html', {'posts': posts, 'query': query})


# Add this new view to your views.py file

@login_required
def check_user_status(request):
    if not hasattr(request.user, 'profile'):
        UserProfile.objects.create(user=request.user, user_type='editor')
        messages.success(request, "Created editor profile for your account.")
    elif request.user.profile.user_type != 'editor':
        request.user.profile.user_type = 'editor'
        request.user.profile.save()
        messages.success(request, "Updated your account to editor status.")
    else:
        messages.info(request, f"Your account already has editor status. Username: {request.user.username}, User type: {request.user.profile.user_type}")
    
    return redirect('dashboard')
