from django.contrib import admin
from .models import CustomUser, Post, Comment, Event, Like, ActivityLog

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'unit', 'date_joined')
    list_filter = ('date_joined', 'unit')
    search_fields = ('username', 'first_name', 'last_name', 'unit')

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content_preview', 'created_at', 'likes_count')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('author__username', 'content')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    
    def likes_count(self, obj):
        return obj.likes.count()

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('author__username', 'text', 'post__content')

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'created_by', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('title', 'location', 'description')

class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'get_display_text', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action')
    readonly_fields = ('timestamp',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Like)
admin.site.register(ActivityLog, ActivityLogAdmin)
