from django import template
from ..models import Post
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


# as @register.simple_tag(name='total_posts'). # if we need to us different name as tag name
@register.simple_tag
def total_posts():
    return Post.objects.count()

@register.simple_tag(name="published_posts")
def published_posts():
    return Post.published.count()

# @register.inclusion_tag('blog/post/latest_post.html')
# @register.simple_tag(name='show_latest_post')
def show_latest_post(count = 5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return{"latest_post": latest_posts}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))