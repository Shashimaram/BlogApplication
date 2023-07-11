from django.contrib import admin
from .models import Post,Comments

class PostAdmin(admin.ModelAdmin):
    # Customize the admin interface for the Post model if needed
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('author',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('-publish', 'status')

admin.site.register(Post, PostAdmin)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name','email', 'post','created', 'active')
    list_filter = ('created', 'active','updated')
    search_fields = ('name', 'email', 'body')

admin.site.register(Comments,CommentsAdmin)
