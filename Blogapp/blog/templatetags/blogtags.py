from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()


# as @register.simple_tag(name='total_posts'). # if we need to us different name as tag name
@register.simple_tag
def total_posts():
    return Post.objects.count()

@register.simple_tag(name="published_posts")
def published_posts():
    return Post.published.count()
