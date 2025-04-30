from django import template

register = template.Library()

@register.filter
def is_editor(user):
    if user.is_authenticated and hasattr(user, 'profile'):
        return user.profile.user_type == 'editor'
    return False