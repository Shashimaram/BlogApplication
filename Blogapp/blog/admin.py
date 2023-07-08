from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published', 'status')
    list_filter = ("status", "created", 'publish','author')
    search_fields = ('title','body')
    raw_id_fields  = ('author')
    date_hierarchy = ('published')
    ordering = ('published', 'status')
    
admin.site.register(Post)
