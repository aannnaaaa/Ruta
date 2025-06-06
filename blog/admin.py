from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'views')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'description', 'content', 'tags')
    date_hierarchy = 'created_at'