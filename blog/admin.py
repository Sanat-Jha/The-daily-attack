from django.contrib import admin
from .models import Post, Tag, UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'user__email')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post)
admin.site.register(Tag)
