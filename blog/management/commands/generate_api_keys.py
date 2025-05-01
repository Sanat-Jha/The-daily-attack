from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import APIKey, Profile

class Command(BaseCommand):
    help = 'Generate API keys for all editor users'

    def handle(self, *args, **options):
        # Get all users with editor profile
        editors = User.objects.filter(profile__user_type='editor')
        
        created_count = 0
        for editor in editors:
            # Check if the editor already has an API key
            if not hasattr(editor, 'api_key'):
                # Create a new API key
                APIKey.objects.create(user=editor)
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created API key for {editor.username}'))
        
        if created_count == 0:
            self.stdout.write(self.style.WARNING('No new API keys were created. All editors already have API keys.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} API keys'))