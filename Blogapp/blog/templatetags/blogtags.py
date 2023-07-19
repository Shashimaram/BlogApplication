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

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


latest_posts=[x for x in Post.published.order_by('-publish')[:5]]

latest_post_urls = [post.get_absolute_url() for post in latest_posts]




@register.simple_tag
def latest_post1():
    return latest_posts[0]

@register.simple_tag
def latest_post2():
    return latest_posts[1] 

@register.simple_tag
def latest_post3():
    return latest_posts[2]

@register.simple_tag
def latest_post4():
    return latest_posts[3]

@register.simple_tag
def latest_post5():
    return latest_posts[4]

@register.inclusion_tag('blog/post/latest_post.html')
# @register.simple_tag(name='show_latest_post')
def show_latest_post(count=1):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {"latest_post_urls": [post.get_absolute_url() for post in latest_posts]}
