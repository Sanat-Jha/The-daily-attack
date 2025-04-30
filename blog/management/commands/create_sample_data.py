from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Tag, UserProfile
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Creates sample data for the blog'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting sample data creation...'))
        
        # Create sample users
        if not User.objects.filter(username='editor').exists():
            editor = User.objects.create_user(
                username='editor',
                email='editor@example.com',
                password='editorpass'
            )
            UserProfile.objects.create(user=editor, user_type='editor')
            self.stdout.write(self.style.SUCCESS('Created editor user'))
        else:
            editor = User.objects.get(username='editor')
            self.stdout.write(self.style.SUCCESS('Editor user already exists'))
            
        if not User.objects.filter(username='viewer').exists():
            viewer = User.objects.create_user(
                username='viewer',
                email='viewer@example.com',
                password='viewerpass'
            )
            UserProfile.objects.create(user=viewer, user_type='viewer')
            self.stdout.write(self.style.SUCCESS('Created viewer user'))
        else:
            self.stdout.write(self.style.SUCCESS('Viewer user already exists'))
        
        # Create sample tags
        tag_names = ['News', 'Technology', 'Sports', 'Politics', 'Entertainment']
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created tag: {tag_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Tag already exists: {tag_name}'))
        
        # Create sample posts
        sample_posts = [
            {
                'title': 'Welcome to The Daily Attack',
                'content': '<p>Welcome to our new blog platform! This is a sample post to get you started.</p><p>Feel free to explore the features and start creating your own content.</p>',
                'status': 'published',
            },
            {
                'title': 'How to Use the Rich Text Editor',
                'content': '<h2>Rich Text Editing</h2><p>Our platform includes a powerful rich text editor that allows you to:</p><ul><li>Format text with <strong>bold</strong>, <em>italic</em>, and other styles</li><li>Insert images and links</li><li>Create lists and tables</li><li>And much more!</li></ul>',
                'status': 'published',
            },
            {
                'title': 'Draft Post Example',
                'content': '<p>This is an example of a draft post. Only editors can see this until it\'s published.</p>',
                'status': 'draft',
            }
        ]
        
        editor = User.objects.get(username='editor')
        
        for post_data in sample_posts:
            if not Post.objects.filter(title=post_data['title']).exists():
                post = Post.objects.create(
                    title=post_data['title'],
                    content=post_data['content'],
                    author=editor,
                    status=post_data['status']
                )
                
                if post.status == 'published':
                    post.published_at = timezone.now()
                    post.save()
                
                # Add random tags
                if tags:  # Make sure we have tags before trying to add them
                    for tag in random.sample(tags, min(random.randint(1, 3), len(tags))):
                        post.tags.add(tag)
                
                self.stdout.write(self.style.SUCCESS(f'Created post: {post.title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Post already exists: {post_data["title"]}'))
        
        self.stdout.write(self.style.SUCCESS('Sample data creation completed'))