# Remove: from django.contrib.auth.decorators import user_passes_test (not used)
from django.shortcuts import redirect
from django.contrib import messages

def editor_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.user_type == 'editor':
            return function(request, *args, **kwargs)
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap