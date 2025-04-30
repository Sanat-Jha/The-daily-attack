from django.utils.deprecation import MiddlewareMixin
from .models import UserProfile

class UserProfileMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and not hasattr(request.user, 'profile'):
            UserProfile.objects.create(user=request.user, user_type='viewer')